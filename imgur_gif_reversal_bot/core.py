# -*- coding: utf-8 -*-
import datetime
import logging
import json
import os
import shutil
import time

from .context import imgur_interface
from .context import gif_reverser

interface = imgur_interface.ImgurInterface()

BUFFER_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 'buffer')
)

def clean_buffer():
    try:
        shutil.rmtree(BUFFER_DIR)
    except FileNotFoundError:
        # nothing to do, no directory to delete
        pass

    os.mkdir(BUFFER_DIR)

def configure_authentication():
    if(interface.is_access_token_refresh_needed()):
        logging.info('refreshing access token...')
        interface.refresh_access_token()
    else:
        logging.info('no need to refresh access token!')
    interface.set_headers()
    # print('client_id headers: ', interface.client_id_headers)
    # print('oauth_headers: ', interface.oauth_headers)

def comment_reversed_gif_on_gallery_gifs(section: str, sort: str, num_pages: int):
    configure_authentication()
    logging.info('getting ' + section + ' ' + sort + ' gifs')
    rising_gifs = interface.get_gallery_page_gifs(section, sort, num_pages)[0]
    # logging.info('rising gifs:')
    # logging.info(json.dumps(rising_gifs, indent=2, sort_keys=True))
    reverser = gif_reverser.GifReverser()
    clean_buffer()
    
    for post in rising_gifs['data']:
        logging.info('-------------------------------------------')
        logging.info('working on post that includes a gif: ' + post['id'])
        logging.debug('post is printed below:\n' \
                + json.dumps(post, indent=2, sort_keys=True))

        if 'images' not in post:
            logging.warn('no images in this post, skipping. Metadata dumped below')
            logging.warn(post)
            continue

        image_to_reverse = None
        for image in post['images']:
            if interface.image_is_gif(image):
                image_to_reverse = image
                break

        if image_to_reverse is None:
            logging.warning('couldn\'t find a gif in post ' + post['id'] + ', skipping.')
            continue

        ### Download image
        logging.info('downloading gif')
        logging.debug('gif metadata:\n' + json.dumps(image_to_reverse,
                                                 indent=2, sort_keys=True))
        image_filename = BUFFER_DIR + '/' + post['id'] + '.mp4'
        interface.download_image(image_to_reverse['id'], image_filename)
        logging.info('gif saved to ' + image_filename)

        ### Reverse video
        logging.info('reversing gif ' + image_filename)
        output_filename = ''.join(image_filename.split('.')[:-1]) + '-reversed.mp4'
        reverser.reverse_gif(image_filename, output_filename)
        logging.info('reversed gif output to ' + output_filename)

        ### upload reversed gif
        logging.info('uploading gif ' + output_filename)
        upload_response = interface.post_reversed_gif(output_filename)
        logging.info('done!')
        logging.debug('response from gif upload:\n' + \
                json.dumps(upload_response, indent=2, sort_keys=True))

        ### checking
        logging.info('checking for when it finishes processing '\
            + '(this can take quite a while)')
        interface.check_if_processing(upload_response['data']['id'])
        # interface.check_if_processing('67VhZNU')

        ### Comment on original post
        logging.info('commenting url to image....')
        comment_response = interface.comment_reversed_gif(post['id'], 
                upload_response['data']['link'])
        logging.info('done!')
        logging.debug('comment response:\n' + \
                json.dumps(comment_response, indent=2, sort_keys=True))

        ### wait 30 seconds between comments to avoid throttling
        logging.info('waiting 30 seconds after commenting to avoid throttling...')
        time.sleep(30)

def main():
    comment_reversed_gif_on_gallery_gifs('user', 'rising', 1)

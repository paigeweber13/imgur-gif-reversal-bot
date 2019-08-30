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

LOG_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 '../logs')
)

def clean_buffer():
    try:
        shutil.rmtree(BUFFER_DIR)
    except FileNotFoundError:
        # nothing to do, no directory to delete
        pass

    os.mkdir(BUFFER_DIR)

    log_filename = BUFFER_DIR + '/log-' + \
            datetime.datetime.now().strftime('%Y-%m-%d_%H%M.%S')
    logging.basicConfig(filename=log_filename, level=logging.INFO)

def set_up_logging():
    # create logs directory
    try:
        os.makedirs(LOG_DIR)
    except FileExistsError:
        # do nothing, folder already exists!
        pass

def configure_authentication():
    if(interface.is_access_token_refresh_needed()):
        logging.info('refreshing access token...')
        interface.refresh_access_token()
    else:
        logging.info('no need to refresh access token!')
    interface.set_headers()
    # print('client_id headers: ', interface.client_id_headers)
    # print('oauth_headers: ', interface.oauth_headers)

def comment_reversed_gif_on_all_rising_gifs():
    configure_authentication()
    print('getting rising gifs')
    rising_gifs = interface.get_rising_gifs()
    filtered = interface.filter_gifs_from_gallery_response(rising_gifs[0])
    reverser = gif_reverser.GifReverser()
    clean_buffer()
    
    for post in filtered['data']:
        logging.info('-------------------------------------------')
        logging.info('working on post that includes a gif:', post['id'])

        image_to_reverse = None
        for image in post['images']:
            if interface.image_is_gif(image):
                image_to_reverse = image
                break

        if image_to_reverse is None:
            logging.warning('couldn\'t find a gif in post', post['id'], ', skipping.')
            continue

        ### Download image
        logging.info('downloading gif')
        logging.info('gif metadata:', image_to_reverse)
        image_filename = BUFFER_DIR + '/' + post['id'] + '.mp4'
        interface.download_image(image_to_reverse['id'], image_filename)
        logging.info('gif saved to ', image_filename)

        ### Reverse video
        logging.info('reversing gif', image_filename)
        output_filename = ''.join(image_filename.split('.')[:-1]) + '-reversed.mp4'
        reverser.reverse_gif(image_filename, output_filename)
        logging.info('reversed gif output to', output_filename)

        ### upload reversed gif
        logging.info('uploading gif', output_filename)
        upload_response = interface.post_reversed_gif(output_filename)
        logging.info('response from gif upload:',
                json.dumps(upload_response, indent=2, sort_keys=True))

        ### checking
        logging.info('checking for when it finishes processing '\
            + '(this can take quite a while)')
        interface.check_if_processing(upload_response['data']['id'])
        # interface.check_if_processing('67VhZNU')

        ### wait 30 seconds between comments to avoid throttling
        time.sleep(30)

        ### Comment on original post
        logging.info('commenting url to image....')
        comment_response = interface.comment_reversed_gif(post['id'], 
                upload_response['data']['link'])
        logging.info('comment response:', 
                json.dumps(comment_response, indent=2, sort_keys=True))

def main():
    set_up_logging()
    comment_reversed_gif_on_all_rising_gifs()

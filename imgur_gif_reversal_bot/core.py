# -*- coding: utf-8 -*-
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
        print('refreshing access token...')
        interface.refresh_access_token()
    else:
        print('no need to refresh access token!')
    interface.set_headers()
    print('client_id headers: ', interface.client_id_headers)
    print('oauth_headers: ', interface.oauth_headers)

def comment_reversed_gif_on_all_rising_gifs():
    configure_authentication()
    print('getting rising gifs')
    rising_gifs = interface.get_rising_gifs()
    filtered = interface.filter_gifs_from_gallery_response(rising_gifs[0])
    reverser = gif_reverser.GifReverser()
    clean_buffer()
    
    for post in filtered['data']:
        print('-------------------------------------------')
        print('working on post that includes a gif:', post['id'])

        image_to_reverse = None
        for image in post['images']:
            if interface.image_is_gif(image):
                image_to_reverse = image
                break

        if image_to_reverse is None:
            print('couldn\'t find a gif in post', post['id'], ', skipping.')
            continue

        ### Download image
        print('downloading gif')
        print('gif metadata:', image_to_reverse)
        image_filename = BUFFER_DIR + '/' + post['id'] + '.mp4'
        interface.download_image(image_to_reverse['id'], image_filename)
        print('gif saved to ', image_filename)

        ### Reverse video
        print('reversing gif', image_filename)
        output_filename = ''.join(image_filename.split('.')[:-1]) + '-reversed.mp4'
        reverser.reverse_gif(image_filename, output_filename)
        print('reversed gif output to', output_filename)

        ### upload reversed gif
        print('uploading gif', output_filename)
        upload_response = interface.post_reversed_gif(output_filename)
        print('response from gif upload:',
                json.dumps(upload_response, indent=2, sort_keys=True))

        ### checking
        print('checking for when it finishes processing '\
            + '(this can take quite a while)')
        interface.check_if_processing(upload_response['data']['id'])
        # interface.check_if_processing('67VhZNU')

        ### wait 30 seconds between comments to avoid throttling
        time.sleep(30)

        ### Comment on original post
        print('commenting url to image....')
        comment_response = interface.comment_reversed_gif(post['id'], 
                upload_response['data']['link'])
        print('comment response:', 
                json.dumps(comment_response, indent=2, sort_keys=True))



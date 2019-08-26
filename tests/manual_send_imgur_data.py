from context import ii

import json
import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
interface = ii.ImgurInterface()
TEST_GALLERY_ID = 'IIeG12c'

def update_auth_if_needed():
    print('configuring authorization')
    if(interface.is_access_token_refresh_needed()):
        print('refreshing access token...')
        interface.refresh_access_token()
    else:
        print('no need to refresh access token!')
    interface.set_headers()

def main():
    update_auth_if_needed()

    #### uploading
    print('uploading a reversed gif...')
    upload_response = interface.post_reversed_gif(ROOT_DIR\
        + '/sample-data/train-tunnel-reversed.mp4')
    print('response from gif upload:',
            json.dumps(upload_response, indent=2, sort_keys=True))

    #### checking
    print('checking for when it finishes processing '\
        + '(this can take quite a while)')
    interface.check_if_processing(upload_response['data']['id'])
    # interface.check_if_processing('67VhZNU')

    #### commenting
    print('commenting url to image....')
    comment_response = interface.comment_reversed_gif(TEST_GALLERY_ID, 
            upload_response['data']['link'])
    print('comment response:', 
            json.dumps(comment_response, indent=2, sort_keys=True))

    #### how to confirm
    print('go to https://imgur.com/gallery/' + TEST_GALLERY_ID, 
            'to check if commenting the reversed gif was successful')

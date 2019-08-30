# -*- coding: utf-8 -*-
"""
the purpose of this file is to test the network parts of this application,
which is basically just configuring authorization and then getting data from
imgur. This data is dumped to disk for manual examination.

Not automated because no one wants to depend on network for automated tests to
succeed.
"""

# from context import imgur_interface
# import context
from context import ii
import os
import json

RESPONSE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 'new-data')
)

interface = ii.ImgurInterface()

def print_stuff_from_rising_respose(rising_response):
    for page in rising_response:
        for post in page['data']:
            # print("###### post", post['title'])
            # print("post['is_ad']:", post['is_ad'])
            # print("post['is_album']:", post['is_album'])
            if 'images' in post:
                for image in post['images']:
                    # if image['type'][:9] == 'image/gif' or \
                    #         image['type'][:5] == 'video':
                    #     print(image['type'])
                    print("image['type']:", image['type'])
                    # print("image['is_ad']:", image['is_ad'])
                    # print("image['has_sound']:", image['has_sound'])
                    # if('mp4' in image):
                    #     print("image['mp4']:", image['mp4'])
                    # if('gifv' in image):
                    #     print("image['gifv']:", image['gifv'])
            #         print()
            # print()


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
    print('client_id headers: ', interface.client_id_headers)
    print('oauth_headers: ', interface.oauth_headers)

    print('getting rising gifs')
    rising_gifs = interface.get_rising_gifs()
    filename = RESPONSE_DIR + '/rising-gifs-response.json'
    with open(filename, 'w') as f:
        json.dump(rising_gifs, f)
        print('response output to ' + filename + ' for manual examination')

    print('downloading first gif')
    first_gif_in_rising_data = rising_gifs[0]['data'][0]['images'][0]
    print('first gif metadata:', first_gif_in_rising_data)
    image_filename = RESPONSE_DIR + '/first-gif-in-rising'
    interface.download_image(first_gif_in_rising_data['id'], image_filename)
    print('first gif saved to ', image_filename)

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
import json
import logging
import os
import random
import requests
import sys

from datetime import datetime
from retrying import retry

API_ROOT = 'https://api.imgur.com/'
# ID where gifs will be added to
ALBUM_ID = 'PO2xwN7'


class ImgurInterface:
    def __init__(self):
        self.auth_filename = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'auth.json'))
        self.keys = {}
        self.headers = {}
        self.get_all_keys_from_json()
        self.set_headers()

    def set_headers(self):
        self.client_id_headers = {
            'Authorization': 'Client-ID ' + self.keys['clientId'],
        }
        self.oauth_headers = {
            'Authorization': 'Bearer ' + self.keys['accessToken'],
        }

    def get_all_keys_from_json(self):
        with open(self.auth_filename, 'r') as f:
            keys = json.load(f)
        self.keys = keys

    def set_all_key_in_json(self):
        with open(self.auth_filename, 'w') as f:
            json.dump(self.keys, f)

    def is_access_token_refresh_needed(self):
        if self.keys['accessToken'] == '':
            return True
        time_since_last_modification = datetime.timestamp(
            datetime.now()) - os.path.getmtime(self.auth_filename)
        # currently, limit is 28 days (minimum month length) because
        # imgur access_tokens expire after a month
        limit_in_ms = 28*24*60*60*1000
        if time_since_last_modification > limit_in_ms:
            return True
        return False

    def refresh_access_token(self):
        access_token_url = API_ROOT + 'oauth2/token'
        request_body = {
            'refresh_token': self.keys['refreshToken'],
            'client_id': self.keys['clientId'],
            'client_secret': self.keys['clientSecret'],
            'grant_type': 'refresh_token'
        }
        r = requests.post(access_token_url, json=request_body)
        response_json = json.loads(r.text)
        self.keys['accessToken'] = response_json['access_token']
        # pretty sure we don't have to update this..... but leaving a comment
        # in for now in case I'm wrong
        # self.keys['refresh_token'] = response_json['refresh_token']
        self.set_all_key_in_json()

    def image_is_gif(self, image_metadata):
        return image_metadata['type'][:9] == 'image/gif' or \
            image_metadata['type'][:5] == 'video'

    def filter_gifs_from_gallery_response(self, response):
        index_of_posts_to_remove = []
        for i in range(len(response['data'])):
            if 'images' in response['data'][i]:
                # response['data'][i] is current post
                response['data'][i]['images'] = [
                    image for image in response['data'][i]['images'] if self.image_is_gif(image)]
                if len(response['data'][i]['images']) == 0:
                    index_of_posts_to_remove.append(i)

        # remove back-to-front so that we dont get 'index out of bounds' error
        # and also so we delete the correct parts of the list.
        index_of_posts_to_remove.reverse()
        for index_of_post_without_gif in index_of_posts_to_remove:
            response['data'].pop(index_of_post_without_gif)
        return response

    def get_rising_gifs(self):
        num_pages_to_get = 1
        responses = []
        # i starts at 1 because imgur starts with page 1
        for i in range(1, num_pages_to_get+1):
            rising_gallery_url = API_ROOT + '3/gallery/user/rising/day/' + \
                str(i) + '?album_previews=true'
            r = requests.get(rising_gallery_url, headers=self.client_id_headers)

            response = json.loads(r.text)
            response = self.filter_gifs_from_gallery_response(response)
            responses.append(response)
        return responses

    def post_reversed_gif(self, path_to_gif: str):
        upload_url = API_ROOT + '3/upload'
        image_name = ('%32x' % random.getrandbits(32)).strip() \
                + path_to_gif.split('/')[-1]
        body = {
            'type': 'file',
            'name': image_name,
            'title': image_name,
            'album': ALBUM_ID,
        }
        files = {
        }
        with open(path_to_gif, 'rb') as f:
            files['video'] = f.read()
        r = requests.post(upload_url, data=body, files=files, 
                headers=self.oauth_headers)
        # print('RESPONSE FROM POSTING REVERSED GIF')
        response_as_dict = json.loads(r.text)
        # print(json.dumps(response_as_dict, indent=2, sort_keys=True))
        return response_as_dict
    
    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def check_if_processing(self, image_id: str):
        get_image_url = API_ROOT + '3/image/' + image_id
        r = requests.get(get_image_url, headers=self.client_id_headers)
        response_as_dict = json.loads(r.text)
        status = response_as_dict['data']['processing']['status']
        # print('response from image get:', response_as_dict)
        logging.info('processing status for image', image_id, ':', status)
        if status != 'completed':
            raise IOError('Image is still processing...')
        return response_as_dict

    def comment_reversed_gif(self, id_of_image_to_comment_on: str,
            url_of_reversed_gif: str):
        comment_url = API_ROOT + '3/comment'
        params = {
            'image_id': id_of_image_to_comment_on,
            'comment': url_of_reversed_gif
        }
        r = requests.post(comment_url, data=params, headers=self.oauth_headers)
        # print('RESPONSE FROM COMMENTING A GIF')
        response_as_dict = json.loads(r.text)
        # print(json.dumps(response_as_dict, indent=2, sort_keys=True))
        return response_as_dict

    def download_image(self, image_id: str, filename: str):
        url = 'https://i.imgur.com/' + image_id + '.mp4'
        r = requests.get(url, headers=self.client_id_headers)

        if r.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=255):
                    if chunk:
                        f.write(chunk)

# -*- coding: utf-8 -*-
import json
import os
import requests
import sys

from datetime import datetime

API_ROOT = 'https://api.imgur.com/'

class ImgurInterface:
    def __init__(self):
        self.auth_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'auth.json'))
        self.keys = {}
        self.get_all_keys_from_json()

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
        self.keys['access_token'] = response_json['access_token']
        # pretty sure we don't have to update this..... but leaving a comment
        # in for now in case I'm wrong
        # self.keys['refresh_token'] = response_json['refresh_token']
        self.set_all_key_in_json()
        
    def get_rising_gifs(self):
        rising_gallery_url = API_ROOT + '3/gallery/user/rising/day/1?album_previews=true'
        headers = {
            'Authorization': 'Client-ID ' + self.keys['clientId'],
        }
        r = requests.get(rising_gallery_url, headers=headers)
        return r.text


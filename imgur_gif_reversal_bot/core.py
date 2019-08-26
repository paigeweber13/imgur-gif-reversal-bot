# -*- coding: utf-8 -*-
from .context import imgur_interface
from .context import gif_reverser

interface = imgur_interface.ImgurInterface()

def configure_authentication():
    if(interface.is_access_token_refresh_needed()):
        print('refreshing access token...')
        interface.refresh_access_token()
    else:
        print('no need to refresh access token!')
    interface.set_headers()
    print('interface headers: ', interface.headers)

def comment_reversed_gif_on_first_rising_gif():
    configure_authentication()
    print('getting rising gifs')
    rising_gifs = interface.get_rising_gifs()
    filtered = interface.filter_gifs_from_gallery_response(rising_gifs)

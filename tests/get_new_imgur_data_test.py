# -*- coding: utf-8 -*-

# from context import imgur_interface
import context

def main():
    interface = context.ii.ImgurInterface()

    print('configuring authorization')
    if(interface.is_access_token_refresh_needed()):
        print('refreshing access token...')
        interface.refresh_access_token()
    else:
        print('no need to refresh access token!')
    
    print('getting rising gifs')
    rising_gifs = interface.get_rising_gifs()
    print(rising_gifs)

if __name__ == '__main__':
    main()
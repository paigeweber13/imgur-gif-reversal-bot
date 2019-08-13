# -*- coding: utf-8 -*-

# from context import imgur_interface
import context

def print_stuff_from_rising_respose(rising_response):
    for page in rising_response:
        for post in page['data']:
            print("###### post", post['title'])
            # print("post['is_ad']:", post['is_ad'])
            # print("post['is_album']:", post['is_album'])
            if 'images' in post:
                for image in post['images']:
                    if image['type'][:9] == 'image/gif' or \
                            image['type'][:5] == 'video':
                        print(image['type'])
                    # print("image['type']:", image['type'])
                    # print("image['is_ad']:", image['is_ad'])
                    # print("image['has_sound']:", image['has_sound'])
                    # if('mp4' in image):
                    #     print("image['mp4']:", image['mp4'])
                    # if('gifv' in image):
                    #     print("image['gifv']:", image['gifv'])
            #         print()
            # print()

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
    print_stuff_from_rising_respose(rising_gifs)

if __name__ == '__main__':
    main()
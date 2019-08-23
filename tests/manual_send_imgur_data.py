from context import ii

import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
interface = ii.ImgurInterface()

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
    print('commenting a reversed gif...')
    interface.post_reversed_gif(ROOT_DIR + '/sample-data/train-tunnel-reversed.mp4')
    # comment_reversed_gif('IIeG12c', )

if __name__ == '__main__':
    main()
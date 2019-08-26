import datetime
import time

from .context import imgur_interface

interface = imgur_interface.ImgurInterface()

def strip_ids_from_gallery_response(gallery_response):
    return [x['id'] for x in gallery_response[0]['data']]

def find_current_time_for_full_rising_refresh():
    start_time = datetime.datetime.now()
    start_ids = set(strip_ids_from_gallery_response(interface.get_rising_gifs()))
    current_ids = start_ids

    # while the current response and the original response have ANYTHING in
    # common
    # TODO: replace with assignment expressions when 3.8 is released
    # see https://www.python.org/dev/peps/pep-0572/
    num_common_posts = 50
    # while(num_common_posts := len(start_ids.intersection(current_ids))):
    while(num_common_posts):
        print("number of common posts: ", num_common_posts)
        print('waiting...')
        time.sleep(73)
        # time.sleep(60)
        print('getting rising gifs again')
        # we could get an exception here.... like ConnectionError?
        # https://2.python-requests.org/en/master/_modules/requests/exceptions/
        current_ids = set(strip_ids_from_gallery_response(interface.get_rising_gifs()))
        num_common_posts = len(start_ids.intersection(current_ids))

    ### TODO:
    # * set rate to something more regular... every 2 minutes?
    #   every one minute is dangerous because that's over the amount of
    #   requests per day I can do.
    # * gather data: number of common posts by minute passed
    # * graph data with seaborne
    end_time = datetime.datetime.now()
    diff = start_time - end_time
    print("time taken to have all new posts:", diff)

def find_hourly_time_to_refresh_rising():
    ### TODO:
    # implement. This will run 'find_current_time_for...' every hour (?) to
    # give us some data across a whole day.
    pass

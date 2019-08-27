import datetime
import time

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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
        # minimum amount of time between requests to not exceed daily limit
        # time.sleep(73)
        time.sleep(120)
        print('getting rising gifs again')
        # we could get an exception here.... like ConnectionError?
        # https://2.python-requests.org/en/master/_modules/requests/exceptions/
        current_ids = set(strip_ids_from_gallery_response(interface.get_rising_gifs()))
        num_common_posts = len(start_ids.intersection(current_ids))

    ### TODO:
    # * gather data: number of common posts by minute passed
    # * graph data with seaborne
    end_time = datetime.datetime.now()
    diff = end_time - start_time
    print("time taken to have all new posts:", diff)
    return diff

def find_hourly_time_to_refresh_rising():
    ### TODO:
    # * implement. This will run 'find_current_time_for...' every hour (?) to
    #   give us some data across a whole day.
    # * graph data with seaborne
    time_taken_by_hour = {}

    for i in range(24):
        while datetime.datetime.now().minute != 0:
            print('not first minute of this hour, waiting...')
            time.sleep(55)
        
        ## First minute of every hour!
        this_hour = datetime.datetime.now().hour
        print('#### HOUR:', this_hour)
        print('Finding time taken to refresh rising....')
        time_taken_by_hour[this_hour] = find_current_time_for_full_rising_refresh()
        
    return time_taken_by_hour

def graph_hourly_time_to_refresh(time_taken_by_hour):
    sns.set(style="white", context="talk")
    x_hours = []
    y_times_taken = []
    for key, value in time_taken_by_hour:
        x_hours.append(key)
        y_times_taken.append(value)
    
    x_hours = np.array(x_hours)
    y_times_taken = np.array(y_times_taken)

    plot = sns.barplot(x=x_hours, y=y_times_taken, palette='vlag')
    plot.savefig('output.png')

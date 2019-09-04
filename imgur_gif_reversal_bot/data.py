import csv
import datetime
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from .context import imgur_interface

interface = imgur_interface.ImgurInterface()

def strip_ids_from_gallery_response(gallery_response):
    return [x['id'] for x in gallery_response['data']]

def find_current_time_for_full_rising_refresh():
    start_time = datetime.datetime.now()
    start_ids = set(strip_ids_from_gallery_response(interface.get_rising_gifs()[0]))
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
        try:
            # minimum amount of time between requests to not exceed daily limit
            # time.sleep(73)
            time.sleep(120)
        except KeyboardInterrupt:
            print('\ncaught KeyboardInterrupt, cancelling and returning elapsed time so far')
            break
        print('getting rising gifs again')
        # we could get an exception here.... like ConnectionError?
        # https://2.python-requests.org/en/master/_modules/requests/exceptions/
        current_ids = set(strip_ids_from_gallery_response(interface.get_rising_gifs()[0]))
        num_common_posts = len(start_ids.intersection(current_ids))

    end_time = datetime.datetime.now()
    diff = end_time - start_time
    print("time taken to have all new posts:", diff)
    return diff

def find_current_time_for_refresh_and_save_to_csv(csv_filename: str):
    start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H%M')
    duration = find_current_time_for_full_rising_refresh()

    if not os.path.exists(csv_filename):
        with open(csv_filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow('timestamp', 'time for refresh')

    with open(csv_filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(start_time, duration)


def find_hourly_time_to_refresh_rising():
    ### DEPRECATED
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

def graph_hourly_time_to_refresh(csv_filename: str):
    # TODO: test
    sns.set(style="white", context="talk")
    x_hours = []
    y_times_taken = []

    with open(csv_filename, 'r') as f:
        for row in f:
            x_hours.append(row[0])
            y_times_taken.append(row[1])
    
    x_hours = np.array(x_hours)
    y_times_taken = np.array(y_times_taken)

    plot = sns.barplot(x=x_hours, y=y_times_taken, palette='vlag')
    plot.savefig('output.png')

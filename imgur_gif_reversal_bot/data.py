import csv
import datetime
import os
import pandas
import plotly.express as px
import time

# import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns

from .context import imgur_interface

interface = imgur_interface.ImgurInterface()


def strip_ids_from_gallery_response(gallery_response):
    return [x['id'] for x in gallery_response['data']]


def find_current_time_for_full_refresh(section: str, sort: str):
    start_time = datetime.datetime.now()
    start_ids = set(strip_ids_from_gallery_response(
        interface.get_gallery_page_gifs('user', 'rising', 1)[0]))
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
            print(
                '\ncaught KeyboardInterrupt, cancelling and returning elapsed'
                ' time so far')
            break
        print('getting rising gifs again')
        # we could get an exception here.... like ConnectionError?
        # https://2.python-requests.org/en/master/_modules/requests/exceptions/
        current_ids = set(strip_ids_from_gallery_response(
            interface.get_gallery_page_gifs(section, sort, 1)[0]))
        num_common_posts = len(start_ids.intersection(current_ids))

    end_time = datetime.datetime.now()
    diff = end_time - start_time
    print("time taken to have all new posts:", diff)
    return diff


def find_current_time_for_refresh_and_save_to_csv(csv_filename: str, section: str, sort: str):
    start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H%M')
    duration = find_current_time_for_full_refresh(section, sort)

    if not os.path.exists(csv_filename):
        print('csv file does not exist, creating...')
        with open(csv_filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'time for refresh'])

    with open(csv_filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([start_time, duration])


def graph_hourly_time_to_refresh(csv_filename: str):
    x_hours = []
    y_times_taken = []

    with open(csv_filename, 'r') as f:
        # skip the header line
        f.readline()
        for row in f:
            row = row.split(',')
            x_hours.append(row[0][11:13])
            time_split = row[1].split(':')
            time_taken = datetime.timedelta(hours=int(time_split[0]),
                                            minutes=int(time_split[1]), seconds=float(time_split[2]))
            y_times_taken.append(time_taken.total_seconds()/60)

    d = {'hour': x_hours, 'time taken (min)': y_times_taken}
    df = pandas.DataFrame(data=d)
    fig = px.histogram(df, x="time taken (min)", nbins=8)
    fig.show()

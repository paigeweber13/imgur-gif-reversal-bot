import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))

from imgur_gif_reversal_bot import data

import json

OUTPUT_FILE = 'output.json'

def main():
    # data.find_current_time_for_full_rising_refresh()
    time_taken_by_hour = data.find_hourly_time_to_refresh_rising()

    with open(OUTPUT_FILE) as f:
        json.dump(time_taken_by_hour, f)
    data.graph_hourly_time_to_refresh(time_taken_by_hour)

if __name__ == '__main__':
    main()
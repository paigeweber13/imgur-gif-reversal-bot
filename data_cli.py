import sys
import json
from imgur_gif_reversal_bot import data
import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))


HOT_VIRAL_REFRESH_CSV = 'data/hot-viral-refresh-times.csv'
USER_RISING_REFRESH_CSV = 'data/user-rising-refresh-times.csv'
HELP_TEXT = 'supply \'c\' for collect or \'g\' for graph as the only argument'


def collect():
    """
    expected usage is putting 'python data_cli.py c' in a crontab, hourly or
    so. 

    all combinations of sections and sorts:

    hot viral
    hot top
    hot time
    top viral
    top top
    top time
    user viral
    user top
    user time
    user rising
    """
    # TODO: implement parallelism so these run simultaneously
    data.find_current_time_for_refresh_and_save_to_csv(
        HOT_VIRAL_REFRESH_CSV, 'hot', 'viral')
    # data.find_current_time_for_refresh_and_save_to_csv(USER_RISING_REFRESH_CSV, 'user', 'rising')


def graph():
    data.graph_hourly_time_to_refresh(USER_RISING_REFRESH_CSV)


def main():
    # data.find_current_time_for_full_rising_refresh()
    if len(sys.argv) < 2:
        print(HELP_TEXT)
        sys.exit(1)

    if sys.argv[1] == 'c':
        collect()
    elif sys.argv[1] == 'g':
        graph()
    else:
        print(HELP_TEXT)


if __name__ == '__main__':
    main()

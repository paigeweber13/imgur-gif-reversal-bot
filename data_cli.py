import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))

from imgur_gif_reversal_bot import data

import json
import sys

OUTPUT_FILE = 'data-output.csv'
HELP_TEXT = 'supply \'c\' for collect or \'g\' for graph as the only argument'

def collect():
    """
    expected usage is putting 'python data_cli.py c' in a crontab, hourly or
    so. 
    """
    data.find_current_time_for_refresh_and_save_to_csv(OUTPUT_FILE)

def graph():
    data.graph_hourly_time_to_refresh(OUTPUT_FILE)

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
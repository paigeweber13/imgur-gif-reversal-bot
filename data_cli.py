import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))

from imgur_gif_reversal_bot import data

def main():
    data.find_current_time_for_full_rising_refresh()
    pass

if __name__ == '__main__':
    main()
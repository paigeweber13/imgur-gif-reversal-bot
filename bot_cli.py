
import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))

from imgur_gif_reversal_bot import core

def main():
    core.comment_reversed_gif_on_all_rising_gifs()

if __name__ == '__main__':
    main()

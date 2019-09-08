from imgur_gif_reversal_bot import core
import datetime
import logging
import os

os.chdir(os.path.abspath(os.path.dirname(__file__)))


LOG_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 'logs')
)


def set_up_logging():
    # create logs directory
    try:
        os.makedirs(LOG_DIR)
    except FileExistsError:
        # do nothing, folder already exists!
        pass

    current_time_string = datetime.datetime.now().strftime('%Y-%m-%d_%H%M.%S')
    log_filename = LOG_DIR + '/log-' + current_time_string + '.log'
    print('logging to', log_filename)
    # CHANGE THIS LINE IF YOU WANT MORE VERBOSE LOGGING
    logging.basicConfig(filename=log_filename, level=logging.INFO)
    logging.info('began logging at ' + current_time_string)


def main():
    set_up_logging()
    core.comment_reversed_gif_on_gallery_gifs('hot', 'viral', 1)


if __name__ == '__main__':
    main()

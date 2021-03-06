import logging
import os
from logging import Formatter
from logging import StreamHandler

DEBUG_FORMAT = (
    "%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d")

LOG_LEVEL = os.environ.get('INPUT_LOGLEVEL', 'WARNING').upper()
# the debug logger is for figuring out what is going on
debug_logger = logging.getLogger("debug")
debug_logger.setLevel(LOG_LEVEL)
debug_logger_file_handler = StreamHandler()
debug_logger_file_handler.setLevel(LOG_LEVEL)
debug_logger_file_handler.setFormatter(Formatter(DEBUG_FORMAT))
debug_logger.addHandler(debug_logger_file_handler)


def getlogger():
    return debug_logger


def main():
    getlogger.error('The TV people are back!')


if __name__ == "__main__":
    main()

"""
    Logger - logging utility
    Written by Lin Liang-Han (qhan)
    Created at 2020.8.16
"""

import logging
import sys
from datetime import datetime
from pytz import timezone, utc


def get_logger(name, save_path="", tz="Asia/Taipei", debug=False):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    formatter = logging.Formatter("[%(levelname)-.1s %(asctime)s %(name)-s] %(message)s", \
                    datefmt="%Y-%m-%d %H:%M:%S")

    if len(logger.handlers) == 0:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    # output logs to file
    if save_path != "":
        file_handler = logging.FileHandler(save_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # set timezone
    def custom_time(*args):
        utc_dt = utc.localize(datetime.utcnow())
        converted = utc_dt.astimezone(timezone(tz))
        return converted.timetuple()

    logging.Formatter.converter = custom_time

    return logger

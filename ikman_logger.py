import logging
from datetime import datetime


class IkmLog(object):
    me = None

    def __new__(cls):  # Make this a singleton
        if cls.me is None:
            cls.me = super(IkmLog, cls).__new__(cls)
            logging.basicConfig(level=logging.NOTSET, filename='ikmanlog.txt')
        return cls.me

    def info(self, msg):
        logging.info(f'[{datetime.now()}] {msg}')

    def warn(self, msg):
        logging.warn(f'[{datetime.now()}] {msg}')

    def critical(self, msg):
        logging.critical(f'[{datetime.now()}] {msg}')


def getlog():
    return IkmLog()

import yaml
from core.config_reader import read
from core import article_reader
import multiprocessing
import nltk
import concurrent.futures
import rx
import time
from rx.core import blockingobservable
import logging
import sys


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def hivut(data):
    logger.info("%s", data)

if __name__ == '__main__':
    data = read('./config/sites.yaml')

    rx.Observable.interval(500).to_blocking().for_each(lambda x: hivut(data))


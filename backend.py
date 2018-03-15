import yaml
from core.config_reader import read
from core import article_reader
import multiprocessing
import nltk
import concurrent.futures
import rx
import time
from rx.core import blockingobservable

def hivut(data):
    print(data)

if __name__ == '__main__':
    data = read('./config/sites.yaml')

    rx.Observable.interval(500).to_blocking().for_each(lambda x: hivut(data))


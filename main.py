from core import config_reader
from core import article_reader
from core import extractor
import hashlib
import logging
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


logging.basicConfig(level=logging.INFO)

def do_work():
    logging.info("Collecting articles using threads")
    articles = article_reader.collect_articles_pool()
    for article in articles:
        curr_article = extractor.to_dict(article)
        curr_article.hash = hashlib.sha256(article.text)

    logging.info("Done deal!")


if __name__ == "__main__":
    logging.info("Starting shit")
    rx.Observable.interval(500).to_blocking().for_each(lambda x: do_work())




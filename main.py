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
    #articles = article_reader.collect_articles()
    for article in articles:
        logging.info("Extracting article")
        curr_article = extractor.to_dict(article, "authors", "canonical_link", "metadata", "meta_description",
                                         "link_hash", "keywords", "meta_img", "meta_keywords", "meta_lang", "movies",
                                         "publish_date", "source_url", "summary", "tags", "text", "title", "top_image",
                                         "url")
        logging.info("Creating hash for current article")
        curr_article["hash"] = hashlib.sha256(article.text.encode("utf-8")).hexdigest()

        logging.info("Current article looks like: {}".format(curr_article))

    logging.info("Done deal!")


if __name__ == "__main__":
    logging.info("Starting shit")
    rx.Observable.interval(20).to_blocking().for_each(lambda x, y: do_work())
   # rx.Observable.interval(20).to_blocking().



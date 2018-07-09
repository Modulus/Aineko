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
from elasticsearch import Elasticsearch


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("Main")
client = Elasticsearch()

def do_work():
    logger.info("Collecting articles using threads")
    articles = article_reader.collect_articles_pool()
    #articles = article_reader.collect_articles()
    for article in articles:
        logger.info("Extracting article")
        curr_article = extractor.to_dict(article, "authors", "canonical_link", "metadata", "meta_description",
                                         "link_hash", "keywords", "meta_img", "meta_keywords", "meta_lang", "movies",
                                         "publish_date", "source_url", "summary", "text", "title", "top_image",
                                         "url")   # TODO: tags is set, convert this to a list


        if type(curr_article) is dict and "text" in curr_article and curr_article["text"]:
            logger.info("Creating hash for current article")
            curr_article["hash"] = hashlib.sha256(article.text.encode("utf-8")).hexdigest()
            logger.info("Saving current article to elasticsearch using link_hash as id")
            client.index(index="articles", doc_type="article", id=curr_article["hash"], body=curr_article)
        else:
            logger.warning("Article does not have text, skipping {}".format(curr_article))

    logger.info("Done deal!")


if __name__ == "__main__":
    logger.info("Starting shit")
    do_work()
    rx.Observable.interval(1000).to_blocking().for_each(lambda x, y: do_work())



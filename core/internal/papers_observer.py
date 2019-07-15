import hashlib

from elasticsearch import Elasticsearch
from rx import Observable, Observer
import logging

from core import extractor

logger = logging.getLogger("PapersObserver")


class PapersObserver(Observer):
    def __init__(self, elasticsearch_url):
        self.elasticsearch_url = elasticsearch_url

    def on_next(self, paper):
        logger.info("Connecting to elasticsearch at {}".format(self.elasticsearch_url))
        client = Elasticsearch([self.elasticsearch_url], sniff_on_start=True, )
        logger.debug("Parsing articles from paper {}".format(paper.url))
        for article in paper.articles:
            logger.debug("Parsing article {}".format(article.url))
            article.parse()
            article.nlp()
            logger.info("Received {0}".format(paper))
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

    def on_completed(self):
        logger.info("Done!")

    def on_error(self, error):
        logger.info("Error Occurred: {0}".format(error))

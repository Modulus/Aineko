import os

from core.config_reader import read
import logging


class Config:

    logger = logging.getLogger("Config")

    def __init__(self, config_path):
        logger = logging.getLogger(Config.__name__)
        logger.info("Reading config data")
        data = read(config_path)
        logger.info("Found data: {}".format(data))
        logger.info("Setting properties")

        self.tags = data["tags"]
        self.urls = data["sites"]
        self.article_fields = ["authors", "canonical_link", "metadata", "meta_description",
                               "link_hash", "keywords", "meta_img", "meta_keywords", "meta_lang", "movies",
                               "publish_date", "source_url", "summary", "tags", "text", "title", "top_image", "url"]

        elasticsearch_url = os.environ["ELASTICSEARCH_URL"]
        if elasticsearch_url:
            self.elasticsearch_url = elasticsearch_url
        else:
            self.elasticsearch_url = data["elasticsearch_url"]

        logger.info("Using elasticsearch at {}".format(self.elasticsearch_url))

        logger.info("Finished creating config object")
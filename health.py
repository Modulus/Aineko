import logging
import time

import numpy as np
import requests
from rx import Observable
import sys
from core.config import Config
from core.internal.sites_observer import SitesObserver

FORMAT = "%(asctime)-15s - %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

logger = logging.getLogger("Main")


config = Config("config/sites.yaml")


def run():
    logger.info("Collecting articles using threads")
    start_time = time.time()

    all_sites = config.urls

    if len(all_sites) <= 0:
        logger.error("Failed to find any sites to scrape")
        sys.exit(1)

    url = "http://{}/_cluster/health".format(config.elasticsearch_url)
    logger.info("Url used for elasticsearch healthcheck: {}".format(url))
    response = requests.get('https://api.github.com/user', auth=('user', 'pass'))
    if 200 != response.status_code:
        logger.error("Failed to connect to healthy elasticsearch")
        sys.exit(1)


    sys.exit(0)


if __name__ == "__main__":
    run()





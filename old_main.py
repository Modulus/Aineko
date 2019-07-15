import logging
import multiprocessing
import time
import requests

import numpy as np
import rx
from rx import Observable

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
    cpu_count = multiprocessing.cpu_count()

    url = "http://{}/_cluster/health".format(config.elasticsearch_url)
    logger.info("Url used for elasticsearch healthcheck: {}".format(url))
    response = requests.get(f"{url}")

    # len(all_sites) > cpu_count and

    if 200 == response.status_code:
        logger.info("Collecting large amount of articles")
        logger.info("Chucking pages to scrape into lists of {} elements".format(cpu_count))
        sites = np.array_split(all_sites, cpu_count)
        source = Observable.from_(sites)

        source.subscribe(SitesObserver(config.elasticsearch_url))

        end_time = time.time()
        logging.info("Started at: %s, ended at: %s, duration: %s", start_time, end_time, end_time - start_time)
    else:
        logging.warn("Ellol")


if __name__ == "__main__":
    logger.info("Starting shit")

    # Run before first interval ( or else you would have to wait x minutes for it to run...)
    run()

    minutes = 60
    ms = minutes * 60 * 1000

    rx.Observable.interval(ms).to_blocking().for_each(lambda x, y: run())
from celery import Celery
import logging
import time
import requests
import os

from core.config import Config
from core.article_reader import collect_and_save_articles

FORMAT = "%(asctime)-15s - %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

logger = logging.getLogger("Main")

redis_url = os.environ["REDIS_URL"]

if not redis_url:
    logger.warning("REDIS_URL environment variable not set. \
         Running with redis://localhost")
    redis_url = "redis://localhost"


app = Celery('tasks', backend=redis_url, broker=redis_url)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    logger.info("Reading Aineko config file")
    config = Config("config/sites.yaml")

    logger.info("Collecting articles using threads")

    all_sites = config.urls

    logger.info(f"Aineko configured with the following urls: {all_sites}")

    # Fetch articles every 5 minutes
    sender.add_periodic_task(20, start.s("config/sites.yaml"),
                             name='read every 10 seconds')


@app.task
def test(arg):
    print(arg)


@app.task
def start(config_file=None):
    config = Config(config_file)

    logger.info("Collecting articles using threads")
    start_time = time.time()

    all_sites = config.urls

    logger.info(all_sites)

    elasticsearch_healthcheck_url = f"http://{config.elasticsearch_url}/_cluster/health"
    logger.info(
        f"Url used for elasticsearch healthcheck: {elasticsearch_healthcheck_url}")
    response = requests.get(f"{elasticsearch_healthcheck_url}")
    logger.info(f"Response {response}")
    if 200 == response.status_code:
        logger.info("Elasticsearch is healthy continue")
        for site in all_sites:
            articles = collect_and_save_articles(site_url=site,
                                                 elasticsearch_url=config.elasticsearch_url, memoize_articles=False)

    # len(all_sites) > cpu_count and

    # if 200 == response.status_code:
    #     logger.info("Collecting large amount of articles")
    # logger.info("Chucking pages to scrape into lists of {}
    # elements".format(cpu_count))

    #     end_time = time.time()
    #     logging.info("Started at: %s, ended at: %s, duration: %s", start_time, end_time, end_time - start_time)
    # else:
    #     logging.warn("Ellol")


@app.task
def read(url):
    logger.info(f"Reading url: {url}")

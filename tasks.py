from celery import Celery, group
from celery.schedules import crontab
import logging
from core.config import Config
from core.article_reader import collect_and_save_articles
from core import extractor
import time
import requests

FORMAT = "%(asctime)-15s - %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

logger = logging.getLogger("Main")

app = Celery('tasks', backend='redis://localhost', broker='redis://localhost')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    logger.info("Reading Aineko config file")
    config = Config("config/sites.yaml")

    logger.info("Collecting articles using threads")

    all_sites = config.urls

    # Fetch articles every 5 minutes
    sender.add_periodic_task(20, start.s("config/sites.yaml"), name='read every 10 seconds')
    # sender.add_periodic_task(10.0, group(read.s(url) for url in all_sites), name="Read url every 10")
    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )


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

    elasticsearch_healthcheck_url = "http://{}/_cluster/health".format(config.elasticsearch_url)
    logger.info("Url used for elasticsearch healthcheck: {}".format(elasticsearch_healthcheck_url))
    response = requests.get(f"{elasticsearch_healthcheck_url}")
    logger.info(f"Response {response}")
    if 200 == response.status_code:
        logger.info("Elasticsearch is healthy continue")
        for site in all_sites:
            articles = collect_and_save_articles(url=site, elasticsearch_url=config.elasticsearch_url, memoize_articles=False)
    
            
            

        
    # len(all_sites) > cpu_count and

    # if 200 == response.status_code:
    #     logger.info("Collecting large amount of articles")
    #     logger.info("Chucking pages to scrape into lists of {} elements".format(cpu_count))

    #     end_time = time.time()
    #     logging.info("Started at: %s, ended at: %s, duration: %s", start_time, end_time, end_time - start_time)
    # else:
    #     logging.warn("Ellol")


@app.task
def read(url):
    logger.info(f"Reading url: {url}")
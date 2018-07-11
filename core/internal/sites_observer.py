import newspaper
from rx import Observable, Observer
import logging

from core.internal.papers_observer import PapersObserver

logger = logging.getLogger("SitesObserver")

memoize_articles = False
threads_per_source = 1


class SitesObserver(Observer):

    def __init__(self, elasticsearch_url):
        self.elasticsearch_url = elasticsearch_url

    def on_next(self, sites):
        print("Received {0}".format(sites))
        papers = []
        for site in sites:
            try:
                logger.info("Collecting data for site: {}".format(site))
                papers.append(newspaper.build(str(site), memoize_articles=memoize_articles))
            except OSError as error:
                logger.error("Failed to build site because of: {}".format(error))

        newspaper.news_pool.set(papers, threads_per_source=threads_per_source)
        newspaper.news_pool.join()
        logger.info("Extracting articles for site {}".format(site))

        source = Observable.from_(papers)

        source.subscribe(PapersObserver(elasticsearch_url=self.elasticsearch_url))

    def on_completed(self):
        print("Done!")

    def on_error(self, error):
        print("Error Occurred: {0}".format(error))


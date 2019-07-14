from core.config_reader import read
import os
import newspaper
import multiprocessing
import logging

logger = logging.getLogger("ArticleReader")


def _collect_sites():
    logger.info("Collecting config from confing/sites.yaml")
    config_path = os.path.dirname(os.path.realpath(__file__))
    sites_file = os.path.join(config_path, os.pardir, 'config', 'sites.yaml')
    sites = read(sites_file)
    if "sites" in sites:
        logger.debug("Found sites, returning")
        return sites["sites"]
    else:
        logger.error("No sites found, returning empty list")
        return []


def check_url(url):
    """
    Check if url can be downloaded
    """
    paper = newspaper.build(url)
    articles = paper.articles
    parsed_articles = []
    if len(articles) > 0:
        for article in articles:
            try:
                article.download()
                article.parse()
                parsed_articles.append(article)
            except newspaper.ArticleException as ex:
                print("Failed to Parse article", ex)
        return len(parsed_articles) > 0
    else:
        return False


def collect_articles():
    sites = _collect_sites()
    article_array = []
    for site in sites:
        logger.info("Collecting articles for site: {}".format(site))
        paper = newspaper.build(site, memoize_articles=False)
        logger.info("Paper: {}".format(paper))
        articles = paper.articles
        logger.info("Found all articles")
        for article in articles:
            try:
                logger.debug("Article url: {}".format(article.url))
                article_array.append(article)
            except newspaper.article.ArticleException as ex:
                logger.error("Failed to extract article {}".format(ex))
    return article_array


def _extract_articles(papers):
    article_array = []
    for paper in papers:
        for article in paper.articles:
            logger.info("Parsing article at {}".format(article.url))
            try:
                article.parse()
                article.nlp()
                article_array.append(article)
            except newspaper.article.ArticleException as ex:
                print(ex)
        return article_array


# TODO: Refactor this to store articles into elasticsearch database on the fly
def collect_articles_pool(memoize_articles=False):
    sites = _collect_sites()
    import numpy as np
    cpu_count = multiprocessing.cpu_count()
    if len(sites) > cpu_count:
        logger.info("Collecting large amount of articles")
        logger.info("Chucking pages to scrape into lists of {} elements".format(cpu_count))
        chunks = np.array_split(sites, cpu_count)
        articles = []
        for chunk in chunks:
            articles + _collect_articles(chunk, memoize_articles, 1)
        logger.info("Finished collecting large number of articles")
        return articles

    elif len(sites) < cpu_count:
        papers = []
        for site in sites:
            logger.info("Collecting data for site: {}".format(site))
            papers.append(newspaper.build(str(site), memoize_articles=memoize_articles))
        logger.info("Finished collecting articles")
        newspaper.news_pool.set(papers, threads_per_source=1)
        newspaper.news_pool.join()
        return _extract_articles(papers)
    else:
        # WTF!!?
        return None


def _collect_articles(sites, memoize_articles=False, threads_per_source=1):
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
    return _extract_articles(papers)

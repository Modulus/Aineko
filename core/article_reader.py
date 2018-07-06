from core.config_reader import read
import os
import newspaper
import multiprocessing
import logging


def _collect_sites():
    logging.info("Collecting config from confing/sites.yaml")
    config_path = os.path.dirname(os.path.realpath(__file__))
    sites_file = os.path.join(config_path, os.pardir, 'config', 'sites.yaml')
    sites = read(sites_file)
    if "sites" in sites:
        logging.debug("Found sites, returning")
        return sites["sites"]
    else:
        logging.error("No sites found, returning empty list")
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
        paper = newspaper.build(site)
        articles = paper.articles
        for article in articles:
            try:
                article_array.append(article)
            except newspaper.article.ArticleException as ex:
                logging.error("Failed to extract article {}".format(ex))
    return article_array


def _extract_articles(papers):
    article_array = []
    for paper in papers:
        for article in paper.articles:
            try:
                article.parse()
                article.nlp()
                article_array.append(article)
            except newspaper.article.ArticleException as ex:
                print(ex)
        return article_array


def collect_articles_pool(memoize_articles=False):
    sites = _collect_sites()
    if len(sites) < multiprocessing.cpu_count():
        papers = []
        for site in sites:
            papers.append(newspaper.build(str(site), memoize_articles=memoize_articles))
        newspaper.news_pool.set(papers, threads_per_source=1)
        newspaper.news_pool.join()
        return _extract_articles(papers)
    else:
        return None

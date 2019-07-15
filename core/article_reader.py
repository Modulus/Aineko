import multiprocessing
import logging
import newspaper
from core import extractor
import hashlib
from elasticsearch import Elasticsearch

logger = logging.getLogger("ArticleReader")


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


# TODO: Refactor this
def collect_and_save_articles(site_url,
                              elasticsearch_url,
                              memoize_articles=False):
    article_array = []
    logger.info("Collecting articles for site: {}".format(site_url))
    paper = newspaper.build(site_url, memoize_articles=memoize_articles)
    logger.info("Paper: {}".format(paper))
    articles = paper.articles
    logger.info("Found all articles")

    # Elasticsearch client in version 7 does not like the port number.
    # Stripping it here

    client = Elasticsearch([elasticsearch_url], sniff_on_start=True, )
    for article in articles:
        try:
            logger.debug("Article url: {}".format(article.url))
            logger.info("Parsing article at {}".format(article.url))
            article.download()
            article.parse()
            article.nlp()
            logger.warning(f"RAW DATA: {article}")
            curr_article = extractor.to_dict(article, "authors",
                                             "canonical_link",
                                             "metadata", "meta_description",
                                             "link_hash", "keywords",
                                             "meta_img", "meta_keywords",
                                             "meta_lang", "movies",
                                             "publish_date", "source_url",
                                             "summary", "text", "title",
                                             "top_image", "url")
            # TODO: tags is set, convert this to a list
            if type(curr_article) is dict and \
                    "text" in curr_article and curr_article["text"]:
                logger.info("Creating hash for current article")
                curr_article["hash"] = hashlib.sha256(
                    article.url.encode("utf-8")).hexdigest()
                logger.info("Saving current article to elasticsearch \
                    using link_hash as id")
                client.index(index="articles", doc_type="article",
                             id=curr_article["hash"],
                             body=curr_article)
                article_array.append(curr_article)
            else:
                logger.warning(f"Article does not have text, \
                    skipping {curr_article}")
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
    sites = []
    import numpy as np
    cpu_count = multiprocessing.cpu_count()
    if len(sites) > cpu_count:
        logger.info("Collecting large amount of articles")
        logger.info(
            f"Chucking pages to scrape into lists of {cpu_count} elements")
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
            papers.append(newspaper.build(str(site),
                                          memoize_articles=memoize_articles))
        logger.info("Finished collecting articles").format(cpu_count)
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
            papers.append(newspaper.build(str(site),
                                          memoize_articles=memoize_articles))
        except OSError as error:
            logger.error("Failed to build site because of: {}".format(error))

    newspaper.news_pool.set(papers, threads_per_source=threads_per_source)
    newspaper.news_pool.join()
    logger.info("Extracting articles for site {}".format(site))
    return _extract_articles(papers)

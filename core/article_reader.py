from core.config_reader import read
import os
import newspaper


def _collect_sites():
    config_path = os.path.dirname(os.path.realpath(__file__))
    sites_file = os.path.join(config_path, os.pardir, 'config', 'sites.yaml')
    sites = read(sites_file)
    if "sites" in sites:
        return sites["sites"]
    else:
        return []

"""

"""
def check_url(url):
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
                article.download()
                article.parse()
                articles.append(article)
            except newspaper.article.ArticleException as ex:
                print(ex)
    return article_array

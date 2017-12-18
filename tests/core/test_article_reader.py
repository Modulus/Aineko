import string

import pytest
import os
from core.article_reader import collect_articles
from core.article_reader import check_url
from core.extractor import convert, extract_url, extract_articles


@pytest.fixture
def sites_file():
    config_path = os.path.dirname(os.path.realpath(__file__))
    sites_file = os.path.join(config_path, os.pardir, 'config', 'sites.yaml')
    return sites_file

# TODO: Check url is irrelevant, remove
# @pytest.mark.parametrize("test_input,expected", [
#     ("http://www.vg.no", False),
#     ("http://vg.no", True),
#     ("http://www.dagbladet.no", False),
#     ("http://dagbladet.no", True),
# ])
# def test_check_url(test_input, expected):
#     assert check_url(test_input) == expected


def test_extract_urls():
    urls = [
        "www.vg.no",
        "https://nettavisen.no"
        "tek.no",
        "cnn.com"
    ]

    result = convert(urls)
    assert len(result) > 0
    assert len(result) == len(urls)
    for url in result:
        assert url.startswith("http://") or url.startswith("https://")


# TODO: lag property based testing av dette
def test_extract_article_based_on_tags():
    from newspaper import Article

    article = Article("http://www.vg.no", "mockpage", "http://www.vg.no")
    keys = ["balle", "klorin", "Kjeks"]
    article.set_keywords(keys)

    article2 = Article("http://www.vg.no", "mockpage", "http://www.vg.no")
    keys2 = ["sommer", "sjø", "pollen"]
    article2.set_keywords(keys2)

    result = extract_articles([article, article2], ["fjøs", "Kjeks"])

    assert len(result) > 0

    r_article = result[0]
    assert r_article.keywords == keys
    assert r_article.url == "http://www.vg.no"
    assert r_article.title == "mockpage"
    assert r_article.source_url == "http://www.vg.no"

    result = extract_articles([article, article2], ["fjøs", "Kjeks", "SJØ"])
    assert len(result) == 2






#def test_article_reader(sites_file):
#    articles = collect_articles()
 #   assert articles is not None

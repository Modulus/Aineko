from newspaper import Article
from faker import Faker
from core import extractor


def test_convert_to_dict_has_url_no_other_gets_result_with_url_and_source_url():
    faker = Faker()

    source = Article(url=faker.url())

    result = extractor.to_dict(source, "article_html", "authors", "images",
                               "keywords", "meta_data", "source_url",
                               "summary", "top_image", "url", "tags",
                               "meta_favicon")
    assert len(result) >= 2
    assert "url" in result
    assert "source_url" in result


def test_convert_to_dict_most_fields_works():
    faker = Faker()

    source = Article(url=faker.url())

    source.authors = [faker.name(), faker.name()]
    source.top_image = faker.image_url()
    source.article_html = faker.text()
    source.images = [faker.image_url(), faker.image_url()]
    source.meta_data = [faker.city(), faker.state(), faker.country()]

    result = extractor.to_dict(source, "article_html", "authors", "images",
                               "keywords", "meta_data", "source_url",
                               "summary", "top_image", "url", "tags",
                               "meta_favicon")

    assert result
    assert len(result) == 7

    assert "article_html" in result
    assert "authors" in result
    assert "images" in result
    assert "keywords" not in result
    assert "meta_data" in result
    assert "source_url" in result
    assert "summary" not in result
    assert "top_image" in result
    assert "url" in result
    assert "tags" not in result
    assert "meta_favicon" not in result

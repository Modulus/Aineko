#from newspaper import Article
#from faker import Faker
#from core.internal import article

#def test_convert_to_dict():
#    faker = Faker()
#
#    source = Article(url=faker.url())
#
#    source.authors = [faker.name(), faker.name()]
#    source.top_image = faker.image_url()
#    source.article_html = faker.text()
#    source.images = [faker.image_url(), faker.image_url()]
#    source.meta_data = [faker.city(), faker.state(), faker.country()]
#
#    result = article.to_dict(source, "article_html", "authors", "images", "keywords", "meta_data", "source_url", "summary", "top_image", "url", "tags", "meta_favicon")
#
#    assert result
#    assert len(result) == 7

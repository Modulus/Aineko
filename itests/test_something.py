from core.article_reader import collect_and_save_articles

def test_something():
    elasticsearch_url = "localhost:9200"
    collect_and_save_articles("http://vg.no", elasticsearch_url=elasticsearch_url)
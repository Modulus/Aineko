import yaml
from core.config_reader import read
from core import article_reader
import multiprocessing
import nltk

if __name__ == '__main__':
    data = read('./config/sites.yaml')
    x = [1,2,3,4,5,6,7,8,9]
    print(x[::11000])
    print(data)
    print(multiprocessing.cpu_count())
    articles = article_reader.collect_articles_pool()

    for article in articles:
        print(article)


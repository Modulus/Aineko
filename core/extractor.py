import logging

logger = logging.getLogger("Extractor")

def convert(data):
    """
    Take a list or single url string and convert it to valid url for the newspaper framework
    """
    if type(data) is list:
        return [extract_url(url) for url in data if type(url) is str and len(url) > 0]
    elif type(data) is str:
        return extract_url(data)
    else:
        raise TypeError("Input needs to be list")


def extract_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return f"http://{url}"
    else:
        return url


def extract_articles(articles, keywords):
    r_articles = []
    for article in articles:
        for keyword in map(str.lower, keywords):
            if keyword in map(str.lower, article.keywords):
                r_articles.append(article)

    return r_articles


def to_dict(article, *args):
    if args:
        data = {key: convert_value(value) for key, value in article.__dict__.items() if key in args and value }
        return data
    else:
        return dict(filter(lambda prop : prop in args, article.__dict__.items()))


def convert_value(value):
    if type(value) is set:
        logger.debug("Converting set to list")
        return list(value)
    else:
        logger.debug("Conversion not necessary, returning as is")
        return value
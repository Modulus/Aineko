from core.redis.redis_handler import RedisHandler

def test_reader():
    urls = [
        "www.vg.no",
        "https://nettavisen.no"
        "tek.no",
        "cnn.com",
        "http://itavisen.no",
        "http://engadget.com",
        "http://boingboing.com",
        "http://ign.com",
        "https://arstechnica.com/",
    ]

    handler = RedisHandler(host="localhost")
    handler.write(urls=urls)


#    saved = handler.read(len(urls))

   # assert len(saved) == len(urls)

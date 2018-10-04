import redis
import logging


logger = logging.getLogger("RedisHandler")


class RedisHandler(object):
    def __init__(self, host="localhost", port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db)

    def write(self, key="urls", urls=None):
        logger.debug("Writing keys {}", urls)
        self.client.sadd(key, *urls)
        self.client.flushall()

    def read(self, key="urls", amount=1):
        urls = []
        for i in range(0, amount):
            urls = self.client.spop(key)
        return urls



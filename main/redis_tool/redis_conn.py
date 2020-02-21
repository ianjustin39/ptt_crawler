import redis


class RedisConn:

    def __init__(self, host, port, db):
        self.redis_conn = redis.Redis(host=host, port=port, decode_responses=True, db=db)

    def set(self, key):
        self.redis_conn.set(key, '0')

    def get(self, key):
        return self.redis_conn.get(key)

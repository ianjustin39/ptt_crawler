import hashlib


def get_redis_key(url):
    data = url
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    key = m.hexdigest()
    return key


def get_mongo_id(url, comment_id):
    data = url + comment_id
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    _id = m.hexdigest()
    return _id

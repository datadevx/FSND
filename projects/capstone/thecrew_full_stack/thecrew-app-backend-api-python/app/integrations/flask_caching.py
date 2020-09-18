from flask import current_app
from redis import Redis, exceptions


def redis_is_available():
    return redis_is_not_available() == False


def redis_is_not_available():
    pong = None
    try:
        redis_client = Redis.from_url(current_app.config['CACHE_REDIS_URL'])
        pong = redis_client.ping()
    except exceptions.ConnectionError:
        return True
    return not pong

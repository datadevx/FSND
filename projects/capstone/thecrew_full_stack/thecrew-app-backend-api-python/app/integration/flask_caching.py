from redis import exceptions
from app import cache


def redis_is_not_available():
    @cache.memoize()
    def test_memoize():
        return "memoize"

    try:
        test_memoize()
        cache.delete_memoized(test_memoize)
    except exceptions.ConnectionError:
        return True
    return False


def delete_memoized(f, *args, **kwargs):
    try:
        cache.delete_memoized(f, args, kwargs)
    except exceptions.ConnectionError:
        pass

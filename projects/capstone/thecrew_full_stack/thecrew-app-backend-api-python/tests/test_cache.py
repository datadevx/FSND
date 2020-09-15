import unittest
from datetime import datetime
from tests import BaseAPITestCase
from app import cache
from app.models import Movie


class CacheTestCase(BaseAPITestCase):
    def test_cache_is_enabled(self):
        from flask_caching.backends.rediscache import RedisCache
        self.assertTrue(
            isinstance(self.app.extensions['cache'][cache], RedisCache))

    def test_cache_type(self):
        self.assertEqual(self.app.config['CACHE_TYPE'], 'redis')

    def test_cache_timeout(self):
        self.assertEqual(self.app.config['CACHE_DEFAULT_TIMEOUT'], 300)

    def test_cache_redis(self):
        self.assertIsNotNone(self.app.config['CACHE_REDIS_URL'])

    def test_can_cache(self):
        movie = Movie(title='Dil Bechara', release_date=datetime(2020, 7, 24))
        cache.add('new_movie', movie)
        self.assertEqual(cache.get('new_movie').title, 'Dil Bechara')
        self.assertEqual(
            cache.get('new_movie').release_date.date(),
            datetime(2020, 7, 24).date())


if __name__ == '__main__':
    unittest.main()

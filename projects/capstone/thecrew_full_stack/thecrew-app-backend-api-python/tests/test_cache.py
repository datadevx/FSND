import unittest
from app import create_app, cache


class CacheTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_cache_is_enabled(self):
        from flask_caching.backends.simplecache import SimpleCache
        self.assertTrue(
            isinstance(self.app.extensions['cache'][cache], SimpleCache))

    def test_cache_type(self):
        self.assertEqual(self.app.config['CACHE_TYPE'], 'simple')

    def test_cache_timeout(self):
        self.assertEqual(self.app.config['CACHE_DEFAULT_TIMEOUT'], 300)

    def test_cache_threshold(self):
        self.assertEqual(self.app.config['CACHE_THRESHOLD'], 1000)

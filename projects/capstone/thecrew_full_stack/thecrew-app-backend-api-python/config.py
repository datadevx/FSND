import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or '280b97464ef14bda8f4623d555339f1b'
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = os.getenv('SQLALCHEMY_RECORD_QUERIES') or True
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    AUTH0_API_AUDIENCE = os.getenv('AUTH0_API_AUDIENCE')
    AUTH0_ALGORITHMS = ['RS256']
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    COMPRESS_MIMETYPES = [
        "text/html",
        "text/css",
        "application/json",
        "application/javascript",
    ]
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_KEY_PREFIX = 'cache.'
    CACHE_REDIS_URL = os.getenv('REDIS_URL')
    THECREW_API_VERSION = os.getenv('THECREW_API_VERSION') or 'v1'
    THECREW_DATE_FORMAT = os.getenv('THECREW_DATE_FORMAT') or '%Y-%m-%d'
    THECREW_OBJECTS_PER_PAGE = os.getenv('THECREW_OBJECTS_PER_PAGE') or 10
    THECREW_LOG_TO_STDOUT = os.getenv('THECREW_LOG_TO_STDOUT')
    THECREW_ADMINS = ['filipebzerra@gmail.com']


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
    AUTH0_GRANT_TYPE = os.getenv('AUTH0_GRANT_TYPE')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or \
        f'sqlite:///{os.path.join(basedir, "data-dev.sqlite")}'


configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

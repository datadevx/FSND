import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or '280b97464ef14bda8f4623d555339f1b'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = os.getenv('SQLALCHEMY_RECORD_QUERIES') or True
    THECREW_OBJECTS_PER_PAGE = os.getenv('THECREW_OBJECTS_PER_PAGE') or 10
    THECREW_API_VERSION = os.getenv('API_VERSION') or 'v1'
    THECREW_AUTH0_DOMAIN = os.getenv(
        'AUTH0_DOMAIN') or 'the-crew-fsnd.us.auth0.com'
    THECREW_AUTH0_ALGORITHMS = ['RS256']
    THECREW_AUTH0_API_AUDIENCE = os.getenv(
        'AUTH0_API_AUDIENCE') or 'thecrew-api'
    DATE_FORMAT = os.getenv('DATE_FORMAT') or '%Y-%m-%d'


class TestingConfig(Config):
    TESTING = True
    PREFERRED_URL_SCHEME = 'https'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or \
        f'sqlite:///{os.path.join(basedir, "data-dev.sqlite")}'


configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

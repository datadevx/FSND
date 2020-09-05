import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or '280b97464ef14bda8f4623d555339f1b'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = os.getenv('SQLALCHEMY_RECORD_QUERIES') or True
    THECREW_API_VERSION = os.getenv('THECREW_API_VERSION') or 'v1'
    THECREW_DATE_FORMAT = os.getenv('THECREW_DATE_FORMAT') or '%Y-%m-%d'
    THECREW_OBJECTS_PER_PAGE = os.getenv('THECREW_OBJECTS_PER_PAGE') or 10
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    AUTH0_API_AUDIENCE = os.getenv('AUTH0_API_AUDIENCE')
    AUTH0_ALGORITHMS = ['RS256']


class TestingConfig(Config):
    TESTING = True
    PREFERRED_URL_SCHEME = 'https'
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

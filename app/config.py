import os

DATABASE_CONNECTION = os.environ.get("DATABASE_CONNECTION")

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "You can't find it"
    CKEDITOR_PKG_TYPE = 'full-all'

    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DATABASE_CONNECTION
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = DATABASE_CONNECTION
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = False

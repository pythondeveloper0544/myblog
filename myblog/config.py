import os

class Config():
    DEBUG = True
    SECRET_KEY = "2e2d00fce190ca46d7a07ff86ff983bd"
    CKEDITOR_PKG_TYPE = 'full-all'
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_CONNECTION"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = False




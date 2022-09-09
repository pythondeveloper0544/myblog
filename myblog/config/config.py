import os

class Config():
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    CKEDITOR_PKG_TYPE = 'full-all'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    HOST = os.environ.get('HOST')
    PORT = '443'


class DevConfig(Config):
    DEBUG = True

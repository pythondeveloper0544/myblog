import os

class Config():
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    CKEDITOR_PKG_TYPE = 'full-all'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False




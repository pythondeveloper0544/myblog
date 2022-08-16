from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor



db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()

login_manager = LoginManager()
login_manager.login_view = 'login'


app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
db.init_app(app)
migrate.init_app(app, db)
ckeditor.init_app(app)
login_manager.init_app(app)

from . import forms, models, routes

    



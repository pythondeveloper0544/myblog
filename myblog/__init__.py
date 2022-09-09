from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from myblog.config import config
from flask_mail import Mail
from os import environ


db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()



def create_app(config_class=config):
    app = Flask(__name__)
    if environ.get('FLASK_DEBUG'):
        app.config.from_object(config_class.DevConfig)
    else:
        app.config.from_object(config_class.ProdConfig)
    db.init_app(app)
    migrate.init_app(app, db)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from myblog.posts.routes import posts
    from myblog.users.routes import users
    from myblog.main.routes import main
    from myblog.admin.routes import admin
    from myblog.errors.routes import errors

    app.register_blueprint(users)
    app.register_blueprint(errors)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(admin)

    return app





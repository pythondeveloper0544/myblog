from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from myblog.config import Config


db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()

login_manager = LoginManager()
login_manager.login_view = 'login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    ckeditor.init_app(app)
    login_manager.init_app(app)

    from myblog.posts.routes import posts
    from myblog.users.routes import users
    from myblog.main.routes import main
    from myblog.errors.routes import errors

    app.register_blueprint(users)
    app.register_blueprint(errors)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app





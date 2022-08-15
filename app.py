from flask import Flask, render_template, url_for, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_ckeditor import CKEditor, CKEditorField
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_required, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from slugify import slugify
from datetime import datetime

from local_settings import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "You can't find it"
app.config['CKEDITOR_PKG_TYPE'] = 'full-all'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ckeditor = CKEditor(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('title', ''))
        super().__init__(*args, **kwargs)
    
    def __repr__(self):
        return self.title 


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(125), unique=True, index=True)
    password_hash = db.Column(db.String(125))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin = db.Column(db.Boolean, default=False)

    @property
    def is_admin(self):
        return self.admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug')
    content = CKEditorField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password1', message='Password must match')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)

@app.route('/create-post', methods=['POST', 'GET'])
@login_required
def create_post():
    form = {}
    if current_user.is_admin:
        form = ArticleForm()
        if form.validate_on_submit():
            article = Article(title=form.title.data, content=form.content.data)
            form.title.data = ''
            form.content.data = ''
            try:
                db.session.add(article)
                db.session.commit()
                return redirect(url_for('posts'))
            except:
                print("Error: Couldn't create post")
    else:
        return abort(403)

    return render_template('create_post.html', form=form)

@app.route('/post/<int:id>/<string:slug>')
@login_required
def post_detail(id, slug):
    article = Article.query.get_or_404(id)
    return render_template('post_detail.html', article=article)

@app.route('/edit-post/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_post(id):
    article = Article.query.get_or_404(id)
    form = ArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.slug = form.slug.data
        article.content = form.content.data
        db.session.add(article)
        db.session.commit()
        return redirect(f'/post/{id}/{article.slug}')
    form.title.data = article.title
    form.slug.data = article.slug
    form.content.data = article.content
    return render_template('edit_post.html', form=form)

@app.route('/delete-post/<int:id>')
@login_required
def delete_post(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
    except:
        print("Error: Couldn't delete post")
    return redirect(url_for('posts'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(username=form.username.data, email=form.email.data)
            user.set_password(form.password1.data)
            db.session.add(user)
            db.session.commit()
            return redirect('/')
  
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/')
        else:
            print("error")

    else:
        print('error')
    return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
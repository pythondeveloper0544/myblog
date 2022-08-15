from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from slugify import slugify
from datetime import datetime
from flask_ckeditor import CKEditor, CKEditorField
from flask_login import LoginManager, login_required

from local_settings import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "You can't find it"
app.config['CKEDITOR_PKG_TYPE'] = 'full-all'

db = SQLAlchemy(app)
ckeditor = CKEditor(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user():
    return None

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('title', ''))
        super().__init__(*args, **kwargs)
    
    def __repr__(self):
        return self.title 


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
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
            "Error: Couldn't add post to database"

    return render_template('create_post.html', form=form)

@app.route('/post/<int:id>/<string:slug>')
def post_detail(id, slug):
    article = Article.query.get_or_404(id)
    return render_template('post_detail.html', article=article)

if __name__ == "__main__":
    app.run(debug=True)
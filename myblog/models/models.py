from flask_login import UserMixin
from slugify import slugify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from myblog import db, login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


post_tag = db.Table('post_tag',
                    db.Column('post_id', db.Integer, db.ForeignKey('article.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                    )


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', passive_deletes=True)
    topic = db.Column(db.Integer, db.ForeignKey('topic.id'))
    tags = db.relationship('Tag', secondary=post_tag, backref="posts")

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('title', ''))
        super().__init__(*args, **kwargs)
    
    def __repr__(self):
        return self.title 


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return self.content[:20]


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True, index=True)
    posts = db.relationship(Article, backref="category")

    def __repr__(self):
        return self.name


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True, index=True)

    def __repr__(self):
        return self.name


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(125), unique=True, index=True)
    password_hash = db.Column(db.String(125))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin = db.Column(db.Boolean, default=False)
    posts = db.relationship(Article, backref="poster", passive_deletes=True)
    comments = db.relationship(Comment, backref="user", passive_deletes=True)

    @property
    def is_admin(self):
        return self.admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username

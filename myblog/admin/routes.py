from flask import Blueprint, render_template, request, redirect, url_for
from myblog.models.models import Users, Topic, Article, Comment
from myblog import db

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def dashboard():
    articles = Article.query.count()
    comments = Comment.query.count()
    users = Users.query.count()
    return render_template('admin/dashboard.html', articles=articles, comments=comments, users=users)

@admin.route('/admin/users')
def users():
    users = Users.query.all()
    if request.method == "POST":
        checked = request.form.get("checked")
    return render_template('admin/users.html', users=users)

@admin.route('/admin/posts')
def posts():
    articles = Article.query.all()
    return render_template('admin/posts.html', articles=articles)

@admin.route('/admin/topics', methods=['GET', 'POST'])
def topics():
    if request.method == "POST":
        name = request.form.get('topic')
        topic = Topic(name=name)
        db.session.add(topic)
        db.session.commit()
        request.form = ''
        return redirect(url_for('admin.topics'))
    topics = Topic.query.all()
    return render_template('admin/topics.html', topics=topics)
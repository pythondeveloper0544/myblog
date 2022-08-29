from flask import Blueprint, render_template, request
from myblog.models import Article, Topic, Tag

main = Blueprint('main', __name__)

@main.context_processor
def context_processor():
    topics = Topic.query.all()
    tags = Tag.query.all()
    return dict(topics=topics, tags=tags)

@main.route('/')
def index():
    articles = Article.query.order_by(Article.date.desc()).limit(3)
    return render_template("main/index.html", articles=articles, active_page='home')


@main.route('/about_me')
def about_me():
    return render_template('main/about_me.html', active_page='about_me')

@main.route('/search', methods=['POST'])
def search():
    searched = request.form.get('q')
    articles = Article.query.filter(Article.content.like('%' + searched + '%')).all()
    return render_template('main/search.html', searched=searched, articles=articles)
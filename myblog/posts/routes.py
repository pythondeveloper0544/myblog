from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user

from myblog import db
from myblog.models import Article, Comment
from myblog.posts.forms import ArticleForm

posts = Blueprint('posts', __name__)

@posts.route('/posts')
def show_posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts/show_posts.html', articles=articles)

@posts.route('/create-post', methods=['POST', 'GET'])
@login_required
def create_post():
    form = {}
    if current_user.is_admin:
        form = ArticleForm()
        if form.validate_on_submit():
            poster = current_user.id
            article = Article(title=form.title.data, poster_id=poster, content=form.content.data)
            form.title.data = ''
            form.content.data = ''
            db.session.add(article)
            db.session.commit()
            flash('New post has been created')
            return redirect(url_for('posts.show_posts'))
    else:
        return abort(403)

    return render_template('posts/create_post.html', form=form)

@posts.route('/post/<int:id>/<string:slug>')
def post_detail(id, slug):
    article = Article.query.get_or_404(id)
    return render_template('posts/post_detail.html', article=article)

@posts.route('/edit-post/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_post(id):
    article = Article.query.get_or_404(id)
    if not article.poster == current_user:
        flash('You can\'t edit this post', "danger")
        return redirect(f'/post/{article.id}/{article.slug}')
    form = ArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.slug = form.slug.data
        article.content = form.content.data
        db.session.add(article)
        db.session.commit()
        flash('Post has been edited')
        return redirect(f'/post/{article.id}/{article.slug}')
    form.title.data = article.title
    form.slug.data = article.slug
    form.content.data = article.content
    return render_template('posts/edit_post.html', form=form)

@posts.route('/delete-post/<int:id>')
@login_required
def delete_post(id):
    article = Article.query.get_or_404(id)
    if not article.poster is current_user:
        flash(f'You can\'t delete this post', "danger")
        return redirect(f'/post/{article.id}/{article.slug}')
    db.session.delete(article)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('posts.show_posts'))

@posts.route('/add-comment/<int:id>', methods=['POST'])
def add_comment(id):
    article = Article.query.get_or_404(id)
    if not current_user.is_authenticated:
        flash("You must login.", "danger")
        return redirect(f'/post/{article.id}/{article.slug}')
    content = request.form.get('comment')
    if content:
        if article:
            comment = Comment(content=content, author=current_user.id, post_id=id)
            db.session.add(comment)
            db.session.commit()
            return redirect(f'/post/{article.id}/{article.slug}')
        else:
            flash("Post does not exist.", "info")
            return redirect(url_for('posts.show_posts'))
    else:
        flash('Comment can\'t be empty.', "danger")
        return redirect(f'/post/{article.id}/{article.slug}')
from flask import render_template, url_for, redirect, abort, flash
from flask_login import login_required, current_user, login_user

from app.models import Article, Users
from app.forms import ArticleForm, RegisterForm, LoginForm
from app import app, db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

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
        flash('Successfully edited')
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
        flash('Post deleted')
    except:
        flash("Couldn't delete post")
    return redirect(url_for('posts'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(username=form.username.data, email=form.email.data)
            user.set_password(form.password1.data)
            db.session.add(user)
            db.session.commit()
            flash('New user syccesfully created')
            return redirect('login')
        else:
            flash('You have an acoount')
            return redirect(url_for('login'))
  
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("You're successfully loggid in!")
            return redirect('/')
        else:
            flash('You must register')
            return redirect('register')

    return render_template('login.html', form=form)

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')


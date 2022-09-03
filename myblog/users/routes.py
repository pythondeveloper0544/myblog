import os
from PIL import Image
import secrets
from pathlib import Path
from flask import Blueprint, redirect, url_for, render_template, flash, current_app, request
from flask_login import login_required, logout_user, login_user, current_user

from myblog import db
from myblog.models.models import Users
from myblog.users.forms import RegisterForm, LoginForm, AccountForm, RequestResetForm, ResetPasswordForm

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', "success")
        return redirect('users.login')
    return render_template('users/register.html', form=form, active_page='register')


@users.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            # flash("You're successfully logged in!", "success")
            flash(f"Welcome {user}!", "success")
            return redirect('/')
        else:
            flash('Login unsuccessfully. Please check email an password again.', "warning")
    return render_template('users/login.html', form=form, active_page='login')


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

def save_image(avatar):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(avatar.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.environ.get("UPLOAD_DIR") + picture_fn
    i = Image.open(avatar)
    size = (100, 100)
    i.thumbnail(size)
    i.save(picture_path)

    return picture_fn

@users.route('/account', methods=["GET", "POST"])
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.avatar:
            picture_path = save_image(form.avatar.data)
            current_user.avatar = picture_path
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    avatar = url_for('static', filename='img/profile/' + current_user.avatar)
    return render_template('users/account.html', form=form, avatar=avatar, active_page="account")

def send_reset_email(mail):
    pass

@users.route('/reset-password')
def reset_request():
    form = RequestResetForm()
    return render_template('users/reset_request.html', form=form)

@users.route('/reset-password/<token>')
def reset_token(token):
    form = ResetPasswordForm()
    return render_template('users/reset_token.html', form=form)
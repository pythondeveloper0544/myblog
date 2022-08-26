from flask import Blueprint, redirect, url_for, render_template, flash, make_response
from flask_login import login_required, logout_user, login_user

from myblog import db
from myblog.models import Users
from myblog.users.forms import RegisterForm, LoginForm

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
        return redirect('login')
    return render_template('users/register.html', form=form)


@users.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You're successfully logged in!", "success")
            return redirect('/')
        else:
            flash('Login unsuccessfully. Please check email an password again.', "warning")
    return render_template('users/login.html', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))
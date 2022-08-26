from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template("main/index.html")


@main.route('/about_me')
def about_me():
    return render_template('main/about_me.html')
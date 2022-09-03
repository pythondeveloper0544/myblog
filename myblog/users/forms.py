from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from myblog.models.models import Users


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password1', message='Passwords must match.')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken.')

    def validate_email(self, email):
        user = Users.query.filter_by(username=email.data).first()
        if user:
            raise ValidationError('This email is taken.')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    avatar = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is taken.')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = Users.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError('This email is taken.')


class RequestResetForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = Users.query.filter_by(username=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email.')


class ResetPasswordForm(FlaskForm):
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password1', message='Passwords must match.')])
    submit = SubmitField('Reset Password')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo


class PostForm(FlaskForm):
    title = StringField('Tittle', validators=[DataRequired()])
    body = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Enter')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enter')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Enter')


class CommentForm(FlaskForm):
    text = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Enter')

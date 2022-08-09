
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange


class UserForm(FlaskForm):
    username = StringField("Enter a Userame*", validators=[
                           DataRequired(), Length(min=2, max=20)])
    email_id = StringField("Email address")
    password_hash = PasswordField("Password*", validators=[
                                  DataRequired(), EqualTo('password_hash2', message='Passwords must match!')])
    password_hash2 = PasswordField(
        "Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class MootsForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Search User")


class AddFavorite(FlaskForm):
    submit = SubmitField("Add favorite")


class TwitterSearchForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    number_of_tweets = IntegerField("Number of Tweets", validators=[DataRequired(),
                                    NumberRange(min=1, max=2000)])
    submit = SubmitField("Submit")

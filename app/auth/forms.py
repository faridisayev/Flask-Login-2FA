from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, ValidationError
from app.models.account import Account
import re

class SignupForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField(validators=[InputRequired(), Regexp(re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{1,80}$"))])
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Signup')

    def validate_username(self, username):
        existing_username = Account.query.filter_by(username = username.data).first()
        if existing_username: raise ValidationError('This username is already taken.')

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    remember_me = BooleanField()
    submit = SubmitField('Login')

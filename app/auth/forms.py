from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp, ValidationError
from app.models.account import Account
import re

class SignupForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Regexp(re.compile(r'^[a-zA-Z0-9_-]{3,20}$'), message = 'The username must consist of alphanumeric characters (letters A-Z in both uppercase and lowercase and digits 0-9), as well as the underscore `_` and hyphen `-`.')])
    email = EmailField(validators=[InputRequired(), Length(max=80)])
    password = PasswordField(validators=[InputRequired(), Regexp(re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,80}$"), message = 'The password must contain at least one digit, one lowercase and one uppercase letter, and it must be between 8 and 80 characters long.')])
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo('password', message = 'This field should be equal to password field.')])

    def validate_username(self, username):
        existing_username = Account.query.filter_by(username = username.data).first()
        if existing_username: raise ValidationError('An account with this username already exists.')

    def validate_email(self, email):
        existing_email = Account.query.filter_by(email = email.data).first()
        if existing_email: raise ValidationError('An account with this email already exists.')

class LoginForm(FlaskForm):
    email_or_username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    remember_me = BooleanField()

class ResetPasswordForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(max=80)])

    def validate_email(self, email):
        existing_email = Account.query.filter_by(email = email.data).first()
        if not existing_email: raise ValidationError('User with this email does not exist.')

class NewPasswordForm(FlaskForm):
    new_password = PasswordField(validators=[InputRequired(), Regexp(re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,80}$"), message = 'The password must contain at least one digit, one lowercase and one uppercase letter, and it must be between 8 and 80 characters long.')])
    confirm_new_password = PasswordField(validators=[InputRequired(), EqualTo('new_password', message = 'This field should be equal to password field.')])

class TOTPLoginForm(FlaskForm):
    totp_digit_1 = IntegerField(validators = [InputRequired()])
    totp_digit_2 = IntegerField(validators = [InputRequired()])
    totp_digit_3 = IntegerField(validators = [InputRequired()])
    totp_digit_4 = IntegerField(validators = [InputRequired()])
    totp_digit_5 = IntegerField(validators = [InputRequired()])
    totp_digit_6 = IntegerField(validators = [InputRequired()])
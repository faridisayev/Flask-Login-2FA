from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from app.models.account import Account

class UpdateAccountForm(FlaskForm):
    username = StringField(validators=[Length(max=20)])
    email = EmailField(validators=[Length(max=80)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        existing_username = Account.query.filter_by(username = username.data).first()
        if existing_username: raise ValidationError('An account with this username already exists.')

    def validate_email(self, email):
        existing_email = Account.query.filter_by(email = email.data).first()
        if existing_email: raise ValidationError('An account with this email already exists.')

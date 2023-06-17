from app.extensions import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    email = db.Column(db.String(80), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)
    created_at = db.Column(db.DateTime(timezone = True), server_default = func.now())
    enabled_2fa = db.Column(db.Boolean, nullable = False, default = False)
    secret_key = db.Column(db.String(80))

    def __repr__(self):
        return f'<Account ID: {self.id}>'
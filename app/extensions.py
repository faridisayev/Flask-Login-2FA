# SQLAlchemy 

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Flask-Limiter

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Flask-Login 

from flask_login import LoginManager
from app.models.account import Account

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please login to continue'
login_manager.login_message_category = 'success'

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

# Flask-Mail

from flask_mail import Mail

mail = Mail()
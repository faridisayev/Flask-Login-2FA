from flask import Flask
from config import Config
from app.extensions import db
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

def create_app(create_config=Config):
    app = Flask(__name__)
    app.config.from_object(create_config)

    db.init_app(app)

    # login manager 

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please login to continue'
    login_manager.login_message_category = 'success'

    from app.models.account import Account

    @login_manager.user_loader
    def load_user(user_id):
        return Account.query.get(int(user_id))
    
    # blueprints

    from app.main import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import bp as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    return app
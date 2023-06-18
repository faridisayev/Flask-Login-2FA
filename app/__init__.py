from flask import Flask, render_template
from config import Config
from app.extensions import db, login_manager, limiter, mail

def create_app(create_config=Config):
    app = Flask(__name__)
    app.config.from_object(create_config)

    db.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)

    # blueprints

    from app.main import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import bp as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # error handlers

    @app.errorhandler(401)
    def Unauthorized(error):
        return render_template('errors/401.html'), 401

    @app.errorhandler(404)
    def NotFound(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(429)
    def TooManyRequests(error):
        return render_template('errors/429.html'), 429

    @app.errorhandler(500)
    def InternalServerError(error):
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(Exception)
    def Unknown(error):
        app.logger.error(str(error))
        return render_template('errors/unknown.html'), 500
    
    return app
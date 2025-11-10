from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from .routes.auth_routes import auth_bp
    from .routes.movie_routes import movie_bp
    from .routes.booking_routes import booking_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(movie_bp, url_prefix="/movies")
    app.register_blueprint(booking_bp, url_prefix="/bookings")

    with app.app_context():
        db.create_all()

    return app

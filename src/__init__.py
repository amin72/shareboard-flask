import os

from flask import Flask
from flask_jwt_extended.jwt_manager import JWTManager

from src.database import db
from src.auth import auth
from src.tickets import tickets, limiter



def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DB_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
    )

    db.init_app(app)

    @app.get('/')
    def home():
        return 'Home Page!'

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(tickets)

    limiter.init_app(app)

    return app

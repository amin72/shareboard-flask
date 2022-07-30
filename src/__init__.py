import os
from flask import Flask
from src.database import db


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

    return app

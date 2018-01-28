from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config


db = SQLAlchemy()


def create_app(config_name='default'):
    app = Flask(__name__)
    app_conf = config[config_name]

    app.config.from_object(app_conf)
    config[config_name].init_app(app)

    db.init_app(app)

    return app

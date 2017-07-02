"""
learn flask app.init
"""
# pylint: disable=invalid-name, too-few-public-methods


from flask import Flask, url_for, redirect, request, render_template, session, flash
from flask_bootstrap import Bootstrap #得先导入Bootsrtap
from flask_mail import Mail, Message
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
mydb = SQLAlchemy()


def create_app(config_name):
    """create app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    mydb.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app

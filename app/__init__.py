"""
learn flask app.init
"""
# pylint: disable=invalid-name, too-few-public-methods


from flask import Flask, url_for, redirect, request, render_template, session, flash
from flask_bootstrap import Bootstrap #得先导入Bootsrtap
from flask_mail import Mail, Message
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
mydb = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    """create app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    mydb.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')


    return app

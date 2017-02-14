# -*- coding: UTF-8 -*-
# flask
from flask import Flask
# plugin
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, \
     login_required, current_user
from flask_principal import Principal, Identity, AnonymousIdentity, \
     identity_changed,identity_loaded,UserNeed,RoleNeed
# config
from config import config

principals = Principal()
login_manager = LoginManager()
db = SQLAlchemy()
session = Session()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)
    principals.init_app(app)
    db.init_app(app)
    session.init_app(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user

        if hasattr(current_user, 'its_id'):
            identity.provides.add(UserNeed(current_user.its_id))

        if hasattr(current_user, 'bbs_signature'):
            identity.provides.add(RoleNeed(current_user.bbs_signature))


    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


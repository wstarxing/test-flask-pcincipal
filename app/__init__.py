# -*- coding: UTF-8 -*-
# flask
from flask import Flask
# plugin
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed
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

    from app.main.principalsource import EditBlogPostNeed

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user

        if hasattr(current_user, 'its_id'):
            identity.provides.add(UserNeed(current_user.its_id))

        if hasattr(current_user, 'roles'):
            for i in current_user.roles:
                identity.provides.add(RoleNeed(i.name))

        if hasattr(current_user, 'posts'):
            for post in current_user.posts:
                identity.provides.add(EditBlogPostNeed(unicode(post.id)))

    from app.main import main
    app.register_blueprint(main)

    return app


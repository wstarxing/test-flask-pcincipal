# -*- coding: UTF-8 -*-
from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed
from flask_login import LoginManager, current_user
from flask import current_app


from app.main.principalsource import EditBlogPostNeed


@identity_loaded.connect_via(current_app)
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
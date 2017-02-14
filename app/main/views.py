# -*- coding: UTF-8 -*-
import datetime
from collections import namedtuple
from functools import partial
from flask import *
from flask_login import LoginManager, login_user, logout_user, \
     login_required, current_user
from flask_principal import Principal, Identity, AnonymousIdentity, \
     identity_changed,identity_loaded, RoleNeed, UserNeed,Permission


from app.main import main

from app.models.user import *

admin_permission = Permission(RoleNeed('admin1'))
user_permission = Permission(UserNeed(169))

@main.route('/abc')
@login_required
# @admin_permission.require()
# @user_permission.require()
def do_articles():
    permission = Permission(RoleNeed('admin'))
    print permission
    if user_permission.can():
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'failed'})


@main.route('/abcd')
@login_required
@admin_permission.require()
def do_articles1():
    return jsonify({'status': 'admin1'})


@main.route('/login', methods=['POST'])
def login():
        datas = {}
        if request.method == 'POST':
            data = request.get_json(force=True)
            username = data['username']
            password = data['password']
            user = User.query.filter_by(its_username=username).first()
            if user and user.verify_password(password):
                login_user(user)
                datas[u'info'] = 'success login !'
                datas[u'status'] = 0
                identity_changed.send(current_app._get_current_object(),
                                      identity=Identity(user.its_id))

            else:
                datas[u'info '] = 'success failed !'
                datas[u'status'] = 1

        return jsonify(datas)


@main.route('/logout', methods=['POST'])
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

        # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return jsonify({'status': 'ok'})


@main.route('/userinfo', methods=['GET'])
@login_required
def useinfo():
    return jsonify({'id': current_user.its_id,
                    'name':current_user.its_username,
                    'role':current_user.bbs_signature
                    })



# -*- coding: UTF-8 -*-

from flask import *
from flask_login import login_user, logout_user, login_required, current_user

from app.main import main
from app.main.principalsource import *
from app.models.user import *


@main.route('/abc')
@login_required
# @admin_permission.require()
# @user_permission.require()
def do_articles():
    # permission = Permission(RoleNeed('admin'))
    # if permission.can():
    if user_permission.can():
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'failed'})


@main.route('/abcd')
@login_required
@admin_permission.require()
def do_articles1():
    return jsonify({'status': 'admin1'})


@main.route('/vip')
@login_required
@vip_permission.require()
def vip():
    return jsonify({'status': 'vip'})


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
def userinfo():
    print session
    return jsonify({'id': current_user.its_id,
                    'name': current_user.its_username,
                    'role': current_user.bbs_signature
                    })


@main.route('/userroles', methods=['GET'])
def userroles():
    role_list = []
    for role in current_user.roles:
        role_list.append(role.name)

    return jsonify({'role': role_list})


@main.route('/roles', methods=['GET'])
def roles():
    role = Role.query.filter_by(id=0).first()
    user_list = []
    print role.user
    for user in role.user:
        user_list.append(user.its_username)
    return jsonify({'user': user_list})


@main.route('/posts', methods=['GET'])
def edit_post():
    post_id = request.args.get('id', '')
    permission = EditBlogPostPermission(post_id)

    if permission.can():
        # Save the edits ...
        return jsonify({'posts': 'ok'})
    else:
        return jsonify({'posts': 'failed'})


@main.route('/getposts', methods=['GET'])
def getpost():
    posts_list = []
    for post in current_user.posts:
        posts_list.append(post.id)
    return jsonify({'posts': posts_list})






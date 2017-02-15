# coding=utf-8
import random, string, os, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app
from flask_login import UserMixin

from app import login_manager, db


def random_str(randomlength=8):  # 生成随机apikey
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(16)))


users_roles = db.Table(u'users_roles',
                            db.Column(u'user_id', db.Integer, db.ForeignKey(u'T_user.its_id')),  # 对应用户id
                            db.Column(u'role_id', db.Integer, db.ForeignKey(u'roles.id')),  # 对应角色id
                        )


class Role(db.Model):
    """Represents Proected roles."""
    __tablename__ = 'roles'

    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))


class User(UserMixin, db.Model):  # User表映射
    __tablename__ = 'T_user'
    its_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    its_username = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String(12))  # 昵称
    # age = db.Column(db.String(3))         #年龄
    img_url = db.Column(db.String, default='http://tuxi.oss-cn-shanghai.aliyuncs.com/static/img/missing_face.png')  # 头像
    # city = db.Column(db.String)
    its_password = db.Column(db.String(128))
    its_mobile = db.Column(db.String, nullable=True)
    its_address = db.Column(db.String, nullable=True)
    its_register_time = db.Column(db.DateTime(), default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    its_update_time = db.Column(db.DateTime(), default=False)
    confirmed = db.Column(db.Boolean, default=False)
    api_key = db.Column(db.String, default=random_str(8))
    bbs_signature = db.Column(db.String(100))

    posts = db.relationship('Posts', backref=db.backref('userposts'))

    roles = db.relationship(
        'Role',
        secondary=users_roles,
        backref=db.backref('user', lazy='dynamic'))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.its_id)

    # 生成令牌
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.its_id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.its_id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.its_password = generate_password_hash(password)

    # 验证hash密码
    def verify_password(self, password):
        return check_password_hash(self.its_password, password)


@login_manager.user_loader
def load_user(its_id):
    return User.query.get(int(its_id))


class Feedback(db.Model):
    __tablename__ = 'T_Feedback'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Integer)
    content = db.Column(db.String(255))
    time = db.Column(db.DateTime(), default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    user_id = db.Column(db.Integer, db.ForeignKey('T_user.its_id'))

    def __repr__(self):
        return self.status


class Posts(db.Model):  # 主贴
    __tablename__ = 'posts'
    __bind_key__ = 'bbs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键

    uuid = db.Column(db.Integer, db.ForeignKey('T_user.its_id'))



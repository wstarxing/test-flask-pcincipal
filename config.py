# -*- coding: UTF-8 -*-
from redis import Redis


class Config:

    rs = Redis(host='192.168.0.203', port=6379, db=8, password='')

    SECRET_KEY = 'B0Zr98j/3yX R~123JX9@98219~#*XSAa1123xsss'
    SESSION_TYPE = u'redis'
    SESSION_REDIS = rs

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1@192.168.0.202:3306/its'
    SQLALCHEMY_BINDS = {
        'bbs': 'mysql+pymysql://root:1@192.168.0.202:3306/bbs'
    }


config = {
    'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    # 'production': ProductionConfig,
    #  'heroku': HerokuConfig,
    #  'unix': UnixConfig,

    'default': DevelopmentConfig
}
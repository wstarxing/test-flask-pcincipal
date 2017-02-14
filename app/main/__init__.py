# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


from flask import Blueprint
main = Blueprint(u'main', __name__)

from app.main import views


# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Blueprint
# from app.main import views

main = Blueprint(u'main', __name__)

from . import views

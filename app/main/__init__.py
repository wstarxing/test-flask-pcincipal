# -*- coding: UTF-8 -*-
import sys

from flask import Blueprint
from app.main import views

main = Blueprint(u'main', __name__)

reload(sys)
sys.setdefaultencoding('utf-8')

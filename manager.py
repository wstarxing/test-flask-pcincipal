# -*- coding: UTF-8 -*-
import sys
from app import create_app

app = create_app('development')

reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
    app.run(debug=True)

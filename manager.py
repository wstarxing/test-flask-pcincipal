# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from app import create_app

app = create_app('default')

if __name__ == '__main__':
    app.run(debug=True, port=8888)

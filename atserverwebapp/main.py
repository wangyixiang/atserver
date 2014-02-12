#!/usr/bin/env python
#coding:utf-8
# Author:  Yixiang.Wang
# Purpose: 
# Created: 2013/9/9

import os
import platform
import sys


from tornado import web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import options
from torndb import Connection

try:
    from atserverwebapp.libs.options import parse_options
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
    from atserverwebapp.libs.options import parse_options

from atserverwebapp.db import Model
from atserverwebapp.urlhandles import handlers

class Application(web.Application):
    def __init__(self):
        setting = dict(debug=options.debug,
                       template_path=os.path.join(os.path.dirname(__file__), "templates")
                       )
        self.db = Connection(host=options.mysql["host"] + ":" + options.mysql["port"],
                             database=options.mysql["database"],
                             user=options.mysql["username"],
                             password=options.mysql["password"]
                             )
        Model.setup_dbs({"db":self.db})
        super(Application, self).__init__(handlers, **setting)
        

def main():
    parse_options()
    
    http_server = HTTPServer(Application())
    http_server.bind(int(options.port), "127.0.0.1")
    http_server.start()
    
    IOLoop.instance().start()
    
if __name__ == '__main__':
    main()
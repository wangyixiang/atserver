#!/usr/bin/env python
#coding:utf-8
# Author:  Yixiang.Wang
# Purpose: 
# Created: 2013/12/6

from tornado import escape
from tornado.escape import utf8
from tornado.options import options
from tornado.web import RequestHandler, HTTPError

from atserverwebapp.db import load_model
import fsjstatus

class FsjJSONHandler(RequestHandler):
    def get(self):
        pass
        
handlers = [(r"/json/fsj", FsjJSONHandler)]

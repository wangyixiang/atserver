#!/usr/bin/env python
# coding:utf-8
# Author:   Yixiang.Wang
# Purpose:  Making the db as package
# Created: 2013/9/9

import sys
import os

sys.path.append(os.path.abspath(
    os.path.join(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".."), "..")))

from atserverwebapp.libs.loader import load

load_model = load("atserverwebapp.db", "Model")

class Model(object):
    _dbs = {}
    
    @classmethod
    def setup_dbs(cls, dbs):
        cls._dbs = dbs
        
    @property
    def dbs(self):
        return self.dbs
    
    @property
    def db(self):
        return self._dbs.get("db", None)
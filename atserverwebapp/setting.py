#!/usr/bin/env python
#coding:utf-8
# Author:  Yixiang.Wang
# Purpose: setting for web app
# Created: 2013/9/9

import platform

if platform.node() == 'atserver':
    debug = False
else:
    debug = True
    loglevel = "INFO"
    
mysql = {
    "host": "atserver",
    "port": "3306",
    "database": "atdb",
    "username": "",
    "password": ""
    }

port = 80
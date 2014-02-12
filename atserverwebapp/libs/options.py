#!/usr/bin/env python
# coding:utf-8
# Author:  Yixiang.Wang
# Purpose: 
# Created: 2013/9/9

import logging
import os

from tornado.options import parse_command_line, options, define

def parse_config_file(path):
    
    config = {}
    execfile(path,config, config)
    
    for name in config:
        if name in options:
            options[name].set(config[name])
        else:
            define(name, config[name])
            
def parse_options():
    _root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    
    try:
        parse_config_file(os.path.join(_root, "setting.py"))
    except Exception, e:
        logging.error("loading setting failed! Exception: %s" % e)
        
    parse_command_line()
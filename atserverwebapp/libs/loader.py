#!/usr/bin/env python
# coding:utf-8
# Author:   Yixiang.Wang
# Purpose:  Making the libs as package
# Created: 2013/9/9

import importlib

_module_instances = {}

def load(root_module, suffix):
    def load_(name):
        name = name.lower()
        key = '%s.%s' % (root_module, name)
        if key not in _module_instances:
            module = importlib.import_module(".%s" % name, root_module)
            cls = getattr(module, "%s%s%s%s" % (
                name[0].upper(), name[1:], suffix[0].upper(), suffix[1:]))
            _module_instances[key] = cls()
            
        return _module_instances[key]
    
    return load_
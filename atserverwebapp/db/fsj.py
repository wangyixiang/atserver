#!/usr/bin/env python
#coding:utf-8
# Author:  Yixiang.Wang
# Purpose: 
# Created: 2013/9/16

import sys
import os


try:
    from atserverwebapp.db import Model
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".." + os.sep + "..")))
    from atserverwebapp.db import Model
    
class FsjModel(Model):
    def get_fsj_status(self):
        rows = self.db.query("""select * from fszmonitor""")
        if rows:
            return rows
        return []
    
if __name__ == "__main__":
    from torndb import Connection
    db = Connection(host="atserver" + ":" + "3306",
                    database="atdb",
                    user="",
                    password=""
                    )
    Model.setup_dbs({"db":db})
    fsjm = fsjModel()
    fsjm.get_fsj_status()
    
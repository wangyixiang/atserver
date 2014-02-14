#!/usr/bin/env python
#coding:utf-8
# Author:  Yixiang.Wang
# Purpose: 
# Created: 2013/9/16

import logging

from tornado import escape
from tornado.escape import utf8
from tornado.options import options
from tornado.web import RequestHandler, HTTPError

from atserverwebapp.db import load_model
import fsjstatus

class FsjHTMLHandler(RequestHandler):
    def get(self):
        statuses = load_model("fsj").get_fsj_status()
        tstatus = []
        if statuses:
            for astatus in statuses:
                status = {}
                status["machine_ip"] = astatus["machineip"]
                status["machine_status"] = astatus["machinestate"]
                status["process_status"] = ""
                status["player_status"] = ""
                status["frequency"] = ""
                status["stream_type"] = ""
                status["update_time"] = astatus["updatetime"]
                status["comment"] = astatus["comment"]
                status["stream_name"] = ""
                status["bandwidth"] = ""
                status["tdt"] = ""
                status["notepad"] = ""
                if status["machine_status"] == fsjstatus.M_S_NONE:
                    status["machine_status"] = fsjstatus.M_S_NONE_STR
                elif status["machine_status"] == fsjstatus.M_S_UNREACHABLE:
                    status["machine_status"] = fsjstatus.M_S_UNREACHABLE_STR
                elif status["machine_status"] == fsjstatus.M_S_FAILURE:
                    status["machine_status"] = fsjstatus.M_S_FAILURE_STR
                elif status["machine_status"] == fsjstatus.M_S_NORMAL:
                    status["machine_status"] = fsjstatus.M_S_NORMAL_STR
                    status["process_status"] = astatus["processstate"]
                    if status["process_status"] == fsjstatus.P_S_NONE:
                        status["process_status"] = fsjstatus.P_S_NONE_STR
                        status["player_status"] = fsjstatus.PL_S_NONE_STR
                        status["frequency"] = ""
                        status["stream_type"] = ""
                        status["update_time"] = astatus["updatetime"]
                        status["comment"] = ""
                        status["stream_name"] = ""
                    elif status["process_status"] == fsjstatus.P_S_NOTEXIST:
                        status["process_status"] = fsjstatus.P_S_NOTEXIST_STR
                        status["player_status"] = fsjstatus.P_S_NOTEXIST_STR
                        status["frequency"] = ""
                        status["stream_type"] = ""
                        status["update_time"] = astatus["updatetime"]
                        status["comment"] = ""
                        status["stream_name"] = ""
                    elif status["process_status"] == fsjstatus.P_S_CRASH:
                        status["process_status"] = fsjstatus.P_S_CRASH_STR
                        status["player_status"] = fsjstatus.P_S_CRASH_STR
                        status["frequency"] = ""
                        status["stream_type"] = ""
                        status["update_time"] = astatus["updatetime"]
                        status["comment"] = ""
                        status["stream_name"] = ""
                    elif status["process_status"] == fsjstatus.P_S_NORMAL:
                        status["process_status"] = fsjstatus.P_S_NORMAL_STR
                        status["player_status"] = astatus["playerstate"]
                        if status["player_status"] == fsjstatus.PL_S_NONE:
                            status["player_status"] = fsjstatus.PL_S_NONE_STR
                        elif status["player_status"] == fsjstatus.PL_S_UNKNOWN:
                            status["player_status"] = fsjstatus.PL_S_UNKNOWN_STR
                        elif status["player_status"] == fsjstatus.PL_S_INVALID:
                            status["player_status"] = fsjstatus.PL_S_INVALID_STR
                        elif status["player_status"] == fsjstatus.PL_S_READY:
                            status["player_status"] = fsjstatus.PL_S_READY_STR
                            status["frequency"] = astatus["frequency"]
                            status["stream_type"] = astatus["streamtype"]
                            status["update_time"] = astatus["updatetime"]
                            status["comment"] = astatus["comment"]
                            status["stream_name"] = astatus["streamname"]
                            status["bandwidth"] = astatus["bandwidth"]
                            status["tdt"] = astatus["tdt"]
                            status["notepad"] = astatus["notepad"]
                        elif status["player_status"] == fsjstatus.PL_S_PAUSE:
                            status["player_status"] = fsjstatus.PL_S_PAUSE_STR
                            status["frequency"] = astatus["frequency"]
                            status["stream_type"] = astatus["streamtype"]
                            status["update_time"] = astatus["updatetime"]
                            status["comment"] = astatus["comment"]
                            status["stream_name"] = astatus["streamname"]
                            status["bandwidth"] = astatus["bandwidth"]
                            status["tdt"] = astatus["tdt"]
                            status["notepad"] = astatus["notepad"]
                        elif status["player_status"] == fsjstatus.PL_S_PLAY:
                            status["player_status"] = fsjstatus.PL_S_PLAY_STR
                            status["frequency"] = astatus["frequency"]
                            status["stream_type"] = astatus["streamtype"]
                            status["update_time"] = astatus["updatetime"]
                            status["comment"] = astatus["comment"]
                            status["stream_name"] = astatus["streamname"]
                            status["bandwidth"] = astatus["bandwidth"]
                            status["tdt"] = astatus["tdt"]
                            status["notepad"] = astatus["notepad"]
                            
#-----------------------------------------------------------------------------#
                else:
                    status["machine_status"] = fsjstatus.M_S_UNKNOWN_STR
                tstatus.append(status)
        self.render("fsz.html", tstatus=tstatus)
    
handlers = [(r"/fsj", FsjHTMLHandler)]
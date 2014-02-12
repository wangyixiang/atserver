# -*- coding: utf-8 -*-
import datetime
import logging
import socket
import torndb

import win32service
import win32serviceutil
import win32api
import win32con
import win32event
import win32evtlogutil
import os

import pywinauto

RUN_AS_A_SERVICE = False

M_S_NONE = 0
M_S_NORMAL = 1
M_S_UNREACHABLE = 2
M_S_FAILURE = 3

P_S_NONE = 0
P_S_NORMAL = 1
P_S_NOTEXIST = 2
P_S_CRASH = 3

PL_S_NONE = 0
PL_S_PLAY = 1
PL_S_PAUSE = 2
PL_S_READY = PL_S_STOP = 3
PL_S_INVALID = 4
PL_S_UNKNOWN = 5

SLEEP_TIME = 5

#MPEG-2 Transport-Stream Player Application

last_update_time = 0

def get_player_info():
    result = {}
    process_name = "StreamXpress.exe"
    image_version = "2.8.0.546"
    c_play_out = "Play-Out"
    c_file = "File"
    c_file_control_id = 0x0000040B
    c_state = "State"
    c_state_control_id = 0x0000040E
    c_state_play = "Play"
    c_state_pause = "Pause"
    c_state_ready = "Ready"
    c_frequncey_control_id = 0x00000412
    c_bandwidth_control_id = 0x000003FF
    c_type_control_id = 0x00000403
    c_tdt_control_id = 0x000003F3
    
    
    try:
        logging.info('starting fetch player info.')
        app_process = pywinauto.Application().connect_(path=process_name)
        result['ms'] = M_S_NORMAL
        result['ps'] = P_S_NORMAL
        parentwindow = app_process.top_window_()
        file_window = app_process.windows_(top_level_only=False, parent=parentwindow.handle, control_id = c_file_control_id)[0]
        state_window = app_process.windows_(top_level_only=False, parent=parentwindow.handle, control_id = c_state_control_id)[0]
        freq_window = app_process.windows_(top_level_only=False, parent=parentwindow.handle, control_id = c_frequncey_control_id)[0]
        stype_window = app_process.windows_(top_level_only=False, parent=parentwindow.handle, control_id = c_type_control_id)[0]
        bandwidth_window = app_process.windows_(top_level_only=False, parent=parentwindow.handle, control_id = c_bandwidth_control_id)[0]
        tdt_window = app_process.windows_(top_level_only=False, parent=parentwindow.handle, control_id = c_tdt_control_id)[0]

        result['pls'] = PL_S_UNKNOWN
        result['stream'] = ''
        result['freq'] = ''
        result['stype'] = ''
        result['bandwidth'] = ''
        result['tdt'] = 0

        if file_window == [] or state_window == [] or stype_window == [] or freq_window == []:
            result['pls'] = PL_S_UNKNOWN
        else:
            file_window_text = file_window.Texts()[0]
            state_window_text = state_window.Texts()[0]
            if file_window_text == '':
                result['pls'] = PL_S_INVALID
            else:
                if  state_window_text == c_state_play:
                    result['pls'] = PL_S_PLAY
                    result['stream'] = file_window_text
                    result['freq'] = freq_window.Texts()[0]
                    result['stype'] = stype_window.Texts()[0]
                    result['bandwidth'] = bandwidth_window.Texts()[0]
                    result['tdt'] = tdt_window.GetCheckState()
                elif state_window_text == c_state_pause:
                    result['pls'] = PL_S_PAUSE
                    result['stream'] = file_window_text
                    result['freq'] = freq_window.Texts()[0]
                    result['stype'] = stype_window.Texts()[0]
                    result['bandwidth'] = bandwidth_window.Texts()[0]
                    result['tdt'] = tdt_window.GetCheckState()
                elif state_window_text == c_state_ready:
                    result['pls'] = PL_S_READY
                    result['stream'] = file_window_text
                    result['freq'] = freq_window.Texts()[0]
                    result['stype'] = stype_window.Texts()[0]
                    result['bandwidth'] = bandwidth_window.Texts()[0]
                    result['tdt'] = tdt_window.GetCheckState()
                else:
                    logging.info("state text is " + state_window_text)
                    result['pls'] = PL_S_UNKNOWN
                    
    except RuntimeError:
        result = { 'ms':M_S_NORMAL, 'ps':P_S_NOTEXIST }
        result['pls'] = PL_S_UNKNOWN
        result['stream'] = ''
        result['freq'] = ''
        result['stype'] = ''
        result['bandwidth'] = ''
        result['tdt'] = 0        

    except pywinauto.application.ProcessNotFoundError:
        result = { 'ms':M_S_NORMAL, 'ps':P_S_NOTEXIST }
        result['pls'] = PL_S_UNKNOWN
        result['stream'] = ''
        result['freq'] = ''
        result['stype'] = ''
        result['bandwidth'] = ''
        result['tdt'] = 0
    except IndexError:
        return None
    logging.info("got all player info.")
    return result


def db_update_fsz_status(fsz_status):
    machinename = socket.gethostname()
    machineip = socket.gethostbyname(machinename)
    machinestate = fsz_status['ms']
    processstate = fsz_status['ps']
    playerstate = fsz_status['pls']
    updatetime = str(datetime.datetime.now())
    streamname = fsz_status['stream']
    streamtype = fsz_status['stype']
    frequency = fsz_status['freq']
    bandwidth = fsz_status['bandwidth'].strip()
    tdt = fsz_status['tdt']
    conn = torndb.Connection("atserver", "atdb", "", "")
    conn.execute("""
    UPDATE fszmonitor
    SET machinename=%s, machinestate=%s, processstate=%s, playerstate=%s,
    updatetime=%s, streamname=%s, streamtype=%s, frequency=%s, bandwidth=%s, 
    tdt=%s
    WHERE machineip=%s
    """, machinename, machinestate, processstate, playerstate,
           updatetime, streamname, streamtype, frequency,
           bandwidth, tdt, machineip
        )
    logging.info("updated the fszmonitor table data.")

#A simple implement for running
def main():
    import time
    logging.getLogger().setLevel(logging.INFO)
    logging.info("status fetcher started.")
    while True:
        logging.info("starting update status.")
        result = get_player_info()
        if result == None:
            logging.info("getting status failed.")
        else:
            db_update_fsz_status(result)
        logging.info("finishing update status.")
        time.sleep(SLEEP_TIME)
    logging.info("status fetcher closed.")
    
    
class transimitterfetcher(win32serviceutil.ServiceFramework):
    _svc_name_ = 'transimitterfetcher'
    _svc_display_name_ = 'transimitterfetcher'
    _svc_description_ = 'transimitter information fetcher'
    
    def __init__(self, args):
        super(self).__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        
    def SvcDoRun(self):
        import time
        logging.getLogger().setLevel(logging.INFO)
        logging.info("status fetcher started.")
        self.timeout = 5000
        while True:
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            if rc == win32event.WAIT_OBJECT_0:
                break;
            else:
                logging.info("starting update status.")
                db_update_fsz_status(get_player_info())
                logging.info("finishing update status.")

        logging.info("status fetcher closed.")

if __name__ == "__main__":
    if RUN_AS_A_SERVICE:
        win32serviceutil.HandleCommandLine(transimitterfetcher)
    else:
        main()

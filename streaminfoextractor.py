#!/usr/bin/env python
#coding:utf-8
# Author:  Yixiang.Wang
# Purpose: 
# Created: 2013/12/12


import filecmp
import hashlib
import logging
import os
import subprocess
import torndb

STREAM_FILE_EXTS = ('.ts','.trp','.mpg')
# EPG_Test.exe (Standard) (source file) (log path) (language code)
# i.e: "FULLSEG" "E:\ch20_515MHz.ts" "e:/EPG_Test/" "jpn"

EPG_TOOL = r'D:\temp\EPG_Test.exe'
#       DVB-T 1SEG FULLSEG
#  DVB-T  Y     N     Y
#   1SEG  N     Y     Y
#FULLSEG  Y     H     Y
#
#STREAM TABLE DEFINITION
#    `filename` VARCHAR(255) NOT NULL,
#    `filesize` BIGINT UNSIGNED NOT NULL,
#    `channelnumber` SMALLINT UNSIGNED,
#    `serverlocation` VARCHAR(1024),
#    `streamtype` VARCHAR(16),
#    `country` VARCHAR(512),
#    `md5` VARCHAR(512),
#    `comment` VARCHAR(512),
#    PRIMARY KEY ( filename, filesize )

#    `toolmd5` VARCHAR(255),
#    `toolret` VARCHAR(64),
#    `toollog` VARCHAR(64)

STREAM_TYPE_DVBT = 'DVB-T'
STREAM_TYPE_1SEG = '1SEG'
STREAM_TYPE_FULLSEG = 'FULLSEG'
BASE_DIR = r'D:'
DVBT_TEMP_DIR = BASE_DIR + os.sep + 'DVTB_LOG'
ONESEG_TEMP_DIR = BASE_DIR + os.sep + '1SEG_LOG'
FULLSEG_TEMP_DIR = BASE_DIR + os.sep + 'FULLSEG_LOG'
LOG_EXT_SUFFIX = '.log'

DEFAULT_SERVER_LOCATION = r'\\fileserver'

db = torndb.Connection("", "atdb", "", "")
toolfile = open(EPG_TOOL)
m = hashlib.md5()
m.update(toolfile.read())
toolmd5 = m.hexdigest()
toolfile.close()
unhandled_file_count = 0

def traverse_dir(target_path, depth=999):

    if depth < 0:
        return
    else:
        depth -= 1
    
    paths = os.listdir(target_path)
    
    for path in paths:
        if path[0] in ('.'):
            continue
        if os.path.isdir(''.join([
            target_path.rstrip(os.sep), 
            os.sep, 
            path])):
            traverse_dir(''.join([target_path.rstrip(os.sep), os.sep, path]), depth)
            continue
        if os.path.splitext(path)[1].lower() not in STREAM_FILE_EXTS:
            continue
        process_file(''.join([target_path.rstrip(os.sep), os.sep, path]))
        
def process_file(src):
    global unhandled_file_count
    try:
        src_filename = os.path.basename(src).decode('gb18030')
        src_size = os.path.getsize(src)
        src_location = os.path.dirname(src).decode('gb18030')
        ret = _triple_run(src)
        toolret = unicode(str(ret[0][0]) + '|' + str(ret[0][1]) + '|' + str(ret[0][2]))
        toollog = unicode(str(ret[1][0]) + '|' + str(ret[1][1]) + '|' + str(ret[1][2]))
        qstr = u"INSERT INTO tempstreams VALUE (%s, %s, %s, %s, %s, %s)"
        db.execute(qstr, *(src_filename, src_size, src_location, toolmd5, toolret, toollog))
    except Exception:
        unhandled_file_count += 1
        logging.error("unhandled file: %s" % src)
        logging.exception(src)

def from_result_to_temp():
    try:
        qstr = u"SELECT * from tempstreams;"
        qresults = db.query(qstr)
    except Exception:
        print "from_result_to_temp fail at start."
        import sys
        sys.exit(-1)
        
    for qresult in qresults:
        qstr = u"INSERT INTO epgtoolresult VALUE (%s, %s , %s ,%s, %s, %s)"
        try:
            src = qresult['serverlocation'] + u'\\' + qresult['filename']
            db.execute(qstr, *(qresult["filename"], qresult["filesize"], qresult["serverlocation"], qresult["toolmd5"], qresult["toolret"], qresult["toollog"]))
        except Exception:
            logging.error("unhandled file: %s" % src)
            logging.exception(src)

def from_db_record():
    try:
        qstr = u"SELECT * FROM epgtoolresult WHERE toolret='0|0|0'"
        qresults = db.query(qstr)
    except Exception:
        print "from_db_record fail at start."
        import sys
        sys.exit(-1)
    
    count = 0
    for qresult in qresults:
        src = (qresult['serverlocation'] + u'\\' + qresult['filename']).encode('gb18030')
        try:
            qstr = u"INSERT INTO tempstreams VALUE (%s, %s, %s, %s, %s, %s)"
            count += 1
            print count
            exist = db.query(u"SELECT * FROM tempstreams WHERE filename=%s and filesize=%s and toolmd5=%s", *(qresult['filename'], qresult['filesize'],toolmd5))
            if len(exist) == 0:
                ret = _triple_run(src)
                toolret = unicode(str(ret[0][0]) + '|' + str(ret[0][1]) + '|' + str(ret[0][2]))
                toollog = unicode(str(ret[1][0]) + '|' + str(ret[1][1]) + '|' + str(ret[1][2]))
                db.execute(qstr, *(qresult['filename'], qresult['filesize'], qresult['serverlocation'], toolmd5, toolret, toollog))
        except Exception:
            logging.error("unhandled file: %s" % src)
            logging.exception(src)
            
def process_file_from_log():
    ude_file = open('unicode_decoded_err.txt')
    ude_data = ude_file.readlines()
    ude_file.close()
    for line in ude_data:
        print line
        process_file(line.strip())
    
def _triple_run(src):
    STANDARD_ARG_DVBT = 'DVBT'
    STANDARD_ARG_1SEG = '1SEG'
    STANDARD_ARG_FULLSEG = 'FULLSEG'
    
    src_filename = os.path.basename(src)
    
    dvbt_ret = subprocess.call([EPG_TOOL, STANDARD_ARG_DVBT, src, DVBT_TEMP_DIR])
    oneseg_ret = subprocess.call([EPG_TOOL, STANDARD_ARG_1SEG, src, ONESEG_TEMP_DIR])
    fullseg_ret = subprocess.call([EPG_TOOL, STANDARD_ARG_FULLSEG, src, FULLSEG_TEMP_DIR])
    
    dvbt_log_file = DVBT_TEMP_DIR + os.sep + src_filename + LOG_EXT_SUFFIX
    oneseg_log_file = ONESEG_TEMP_DIR + os.sep + src_filename + LOG_EXT_SUFFIX
    fullseg_log_file = FULLSEG_TEMP_DIR + os.sep + src_filename + LOG_EXT_SUFFIX
    
    cmp_tuple = [0,0,0]
    if os.path.exists(dvbt_log_file):
        if os.path.exists(oneseg_log_file):
            if filecmp.cmp(dvbt_log_file, oneseg_log_file, 0):
                cmp_tuple[0] = 1
                cmp_tuple[1] = 1
            else:
                cmp_tuple[0] = 1
                cmp_tuple[1] = 2
        else:
            cmp_tuple[0] = 1
    
    if os.path.exists(dvbt_log_file):
        if os.path.exists(fullseg_log_file):
            if filecmp.cmp(dvbt_log_file, fullseg_log_file, 0):
                cmp_tuple[0] = 1
                cmp_tuple[2] = 1
            else:
                cmp_tuple[0] = 1
                cmp_tuple[2] = 3
        else:
            cmp_tuple[0] = 1
            
    if os.path.exists(oneseg_log_file):
        if os.path.exists(fullseg_log_file):
            if filecmp.cmp(oneseg_log_file, fullseg_log_file, 0):
                if cmp_tuple[1] == 0:
                    cmp_tuple[1] = 2
                    cmp_tuple[2] = 2
                else:
                    cmp_tuple[2] = cmp_tuple[1]
            else:
                if cmp_tuple[1] == 0:
                    cmp_tuple[1] = 2
                if cmp_tuple[2] == 0:
                    cmp_tuple[2] == 3
        else:
            cmp_tuple[1] = 2
    
    if cmp_tuple[0] != 0:
        f = open(dvbt_log_file)
        d = f.read()
        if d.strip().lower() == src.lower():
            cmp_tuple[0] = 4
        f.close()
        os.remove(dvbt_log_file)
    if cmp_tuple[1] != 0:
        f = open(oneseg_log_file)
        d = f.read()
        if d.strip().lower() == src.lower():
            cmp_tuple[1] = 4
        f.close()
        os.remove(oneseg_log_file)
    if cmp_tuple[2] != 0:
        f = open(fullseg_log_file)
        d = f.read()
        if d.strip().lower() == src.lower():
            cmp_tuple[2] = 4
        f.close()
        os.remove(fullseg_log_file)
        
    return [ [dvbt_ret,oneseg_ret,fullseg_ret], cmp_tuple ]
            

def parse_tempstreams_log():
    def _handle_it(data, match):
        l = len('2014-01-06 18:36:30,716  ERROR  unhandled file: ')
        data = data[0][l:].strip()
        try:
            ret_dict[match].append(data)
        except:
            logging.exception('')
        
    import re
    ret_dict = {'IntegrityError:':[],'UnicodeDecodeError:':[], 'WindowsError:':[]}
    re_pattern = '^[a-zA-Z]+?:'
    rp = re.compile(re_pattern)
    log_filenames = [r"D:\tempstreams.log",r"D:\2tempstreams.log",r"D:\3tempstreams.log"]
    for log_filename in log_filenames:
        log_file = open(log_filename)
        log_data = log_file.readlines()
        log_file.close()
        temp_lines = []
        for line in log_data:
            temp_lines.append(line)
            m = rp.match(line)
            if m != None:
                _handle_it(temp_lines, m.group(0))
                temp_lines = []
    #dup_file = open('duplicated_file.txt', 'w')
    #ude_file = open('unicode_decoded_err.txt', 'w')
    #we_file = open('windows_err.txt','w')
    #for item in ret_dict['IntegrityError:']:
        #dup_file.write(item + os.linesep)
    #for item in ret_dict['UnicodeDecodeError:']:
        #ude_file.write(item + os.linesep)
    #for item in ret_dict['WindowsError:']:
        #we_file.write(item + os.linesep)
    #dup_file.close()
    #ude_file.close()
    #we_file.close()
    
def sum_dup_file_size():
    filename = r'duplicated_file.txt'
    
if __name__ == '__main__':
    FORMAT = "%(asctime)s  %(levelname)s  %(message)s"
    logging.basicConfig(filename=r'D:\4tempstreams.log', format=FORMAT)
    from_db_record()
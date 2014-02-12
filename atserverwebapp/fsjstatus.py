#!/usr/bin/env python
#coding:utf-8
# Author:  Yixiang.Wang
# Purpose: 
# Created: 2013/9/24

M_S_NONE = 0
M_S_NONE_STR = u"不存在"
M_S_NORMAL = 1
M_S_NORMAL_STR = u"正常"
M_S_UNREACHABLE = 2
M_S_UNREACHABLE_STR = u"无法访问"
M_S_FAILURE = 3
M_S_FAILURE_STR = u"故障中"
M_S_UNKNOWN = 4
M_S_UNKNOWN_STR = u"未知状态"

P_S_NONE = 0
P_S_NONE_STR = u"未安装"
P_S_NORMAL = 1
P_S_NORMAL_STR = u"正常"
P_S_NOTEXIST = 2
P_S_NOTEXIST_STR = u"未运行"
P_S_CRASH = 3
P_S_CRASH_STR = u"已崩溃"

PL_S_NONE = 0
PL_S_NONE_STR = u"未安装"
PL_S_PLAY = 1
PL_S_PLAY_STR = u"播放中"
PL_S_PAUSE = 2
PL_S_PAUSE_STR = u"暂停中"
PL_S_READY = PL_S_STOP = 3
PL_S_READY_STR = PL_S_STOP_STR = u"就绪中"
PL_S_INVALID = 4
PL_S_INVALID_STR = u"无效中"
PL_S_UNKNOWN = 5
PL_S_UNKNOWN_STR = u"未知状态"
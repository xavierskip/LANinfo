#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

class SQL:
    def __init__(self, tablename):
        self.tableName   = tablename
        self.IP_MAC      = "SELECT `ip`,`mac` FROM `%s`  ORDER BY `rowid` ASC" % tablename
        self.count_IP    = "SELECT COUNT(ip) FROM `%s`" % tablename
        self.count_MAC   = "SELECT COUNT(mac) FROM `%s`" % tablename
        self.all_Fields  = "SELECT `rowid`,* FROM `%s` ORDER BY `rowid` ASC" % tablename
        self.select_IP   = "SELECT * FROM `%s` WHERE `ip` = ?" % tablename
        self.update_INFO = "UPDATE `%s` SET name=?,comment=? WHERE ip = ?" % tablename
        self.del_INFO    = "UPDATE `%s` SET mac=Null,time=Null,lastdate=Null WHERE ip = ?" % tablename

    def model(self):
        pass

def frequency(str_time):
    """ return 0:'活跃',1:'使用',2:'占用',3:'离线',4:'废弃',5:'空闲' """
    if str_time == '': return 5
    recent = time.mktime(time.strptime(str_time,'%Y-%m-%d %H:%M:%S'))
    now = time.mktime(time.localtime())
    last = now - recent
    if last<86400:     #one day
        return 0
    elif last<604800:  #one week
        return 1
    elif last<2592000: #one month
        return 2
    elif last<7776000: #three month
        return 3
    elif last<15552000:#half year
        return 4




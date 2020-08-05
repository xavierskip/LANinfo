from __future__ import print_function
from scanner import Scan
from db import database
import ConfigParser
import time
import os
from sqlite3 import OperationalError
from mail import Mail

here = os.path.dirname(os.path.abspath(__file__))
config = ConfigParser.ConfigParser()
config.read(os.path.join(here,'config.ini'))
dbpath = config.get('db','path')
# cover the default abspath config
config.set('db','abspath',os.path.join(here,dbpath))
# simple send mail
u = config.get('mail','username')
p = config.get('mail','password')
smtp = config.get('mail', 'smtp')
mail = Mail(smtp, u, p)
Subject = config.get('mail', 'subject')
Me = config.get('mail', 'from')
You = config.get('mail', 'to')

def saveto(scanner,db):
    cur = db.cur
    # sql
    macTheIP = "SELECT ip FROM `%s` WHERE mac = ?" %scanner.netname
    delmac = "UPDATE `%s` SET mac=Null,time=Null WHERE ip = ?" %scanner.netname
    setMAC = "UPDATE `%s` SET mac=?,time=? WHERE ip = ?" %scanner.netname
    lastTime = "UPDATE `%s` SET lastdate=? WHERE ip = ?" %scanner.netname
    # table exist?
    r = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",(scanner.netname,))
    if not r.fetchone():
        # init database and create table
        db.initTable(config.get('db','schema'),scanner.netname,scanner.iplist)
    for i in scanner.info:
        ip,mac = i
        r = cur.execute(macTheIP,(mac,)).fetchone()
        if r:
            if r[0] == ip:
                cur.execute(lastTime,(get_date(),ip))
            else:
                cur.execute(delmac,(r[0],))
                cur.execute(setMAC,(mac,get_date(),ip))
                message = "[update] %s from %s to %s " %(mac,r[0],ip)
                print(message)
                mail.send(Me, You, Subject, message)
                #logging.debug("[update] %s from %s to %s " %(mac,r[0],ip))
        else:
            cur.execute(setMAC,(mac,get_date(),ip))
            message = "[set] %s to %s " %(mac,ip)
            print(message)
            mail.send(Me, You, Subject, message)
            #logging.debug("[set] %s to %s " %(mac,ip))
    # sql = "INSERT or REPLACE INTO `%s` (ip,mac) VALUES(?,?)" %scanner.netname
    # db.cur.executemany(sql,info)
    db.commit()

def get_date():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def main():
    scanner = Scan(config.get('scan','dest'))
    config.set('db','netname',scanner.netname)
    try:
        db = database(config.get('db','path'))
    except OperationalError, e:
        # init dabase
        os.makedirs('/'.join(config.get('db','path').split('/')[:-1]))
        db = database(config.get('db','path'))
        schame = config.get('db','schema')
        tablename = config.get('db','netname')
        db.initTable(schame,tablename,scanner.iplist)
    # scan start
    start = time.time()
    scanner.do()
    saveto(scanner,db) # save to the database
    print("[time] %1.2fs" %(time.time() - start), end="  ")
    with open('config.ini','wb') as c:
        config.write(c)

if __name__ == '__main__':
    main()
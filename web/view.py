#!/usr/bin/env python
# -*- coding:utf-8 -*-
from web import app
from flask import g, request, render_template, abort, session, redirect, url_for,make_response
#
from db import database
from scanner import win_mac, Scan, ip2int, int2ip
from run import saveto,config
# import logging
import models
import re

SQL = models.SQL(config.get('db','netname'))

from hashlib import sha256
def encrypt_password(password, salt=None):
    if not salt:
        from os import urandom
        salt = urandom(8)
    result = password
    for i in range(3):
        result = sha256(password + salt).digest()
    return result, salt
#
from functools import wraps
def authorize(fn):
    @wraps(fn)
    def wrapper(*args, **kwds):
        state = session.get('logged_in', None)
        if state:
            return fn(*args, **kwds)
        else:
            return redirect(url_for('login',next=request.path))

    return wrapper

@app.before_request
def before_request():
    g.db = database(config.get('db','abspath'))

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

# pages
@app.route('/')
@authorize
def index():
    r = g.db.cur.execute(SQL.IP_MAC)
    if r:
        info = []
        for row in g.db.cur.fetchall():
            # clear the None value
            row = map(lambda x: x if x else '', row)
            info.append(dict(ip=row[0], mac=row[1]))
        amount = g.db.cur.execute(SQL.count_IP).fetchone()[0]
        taken  = g.db.cur.execute(SQL.count_MAC).fetchone()[0]
        return render_template('index.html', info=info, title=SQL.tableName, taken=taken, amount=amount)
    else:
        return redirect(url_for('about'))

@app.route('/detail')
@authorize
def detail():
    r = g.db.cur.execute(SQL.all_Fields)
    if r:
        info = []
        for row in g.db.cur.fetchall():
            # clear the None value
            row = map(lambda x: x if x else '', row)
            lastdate = models.frequency(row[6])
            info.append(dict(num=row[0], ip=row[1], mac=row[2], name=row[3], comment=row[4], time=row[5], lastdate=lastdate))
        return render_template('detail.html', info=info, title=SQL.tableName)
    else:
        return redirect(url_for('about'))

@app.route('/tools')
@authorize
def tools():
    return render_template('tools.html',title="tools",netname=SQL.tableName)

@app.route('/about')
@authorize
def about():
    return render_template('readme.html')

@app.route('/signin', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        referrer = request.args.get('next','/')
        return render_template("login.html",next=referrer)
    if request.method == 'POST': 
        u = request.form['username']
        p = encrypt_password(request.form['password'], app.config['SALT'])[0]
        next = request.form['next']
        if u == app.config['USERNAME'] and p == app.config['PASSWORD']:
            session['logged_in'] = True
            return redirect(next)
        else:
            return render_template('login.html', next=next,error=u'错误的用户名或者密码！')

@app.route('/signout', methods=['GET','POST'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/ip/<ip>')
@authorize
def userip(ip):
    try:
        int_ip = ip2int(ip)
    except Exception, e:
        return "illegal IP address"
    s = Scan(config.get('scan','dest'))
    if s.net_id<int_ip<s.broadcast:
        previous = 0
        next = 0
        if int_ip-1 != s.net_id:
            previous = int2ip(int_ip-1)
        if int_ip+1 != s.broadcast:
            next = int2ip(int_ip+1)
        r = g.db.cur.execute(SQL.select_IP, (ip,)).fetchone()
        if r:
            ip, mac, name, comment, time, lastdate = map(lambda x: x if x else '', r)
            item = {'ip':ip,'mac':mac,'name':name,'comment':comment,'time':time,'lastdate':lastdate}
            return render_template('single.html', item=item, previous=previous, next=next, ip=ip, title=ip)
        else:
            return "not fond!"
    else:
        return "IP out of range!"

# API
@app.route('/get', methods=['GET'])
@authorize
def getmac():
    mac = request.args.get('mac')
    if mac:
        mac =  mac.encode()
        r = g.db.cur.execute(SQL.select_MAC, (mac,)).fetchone()
        if r:
            return ','.join(map(lambda x: str(x) if x else '', r))
        else:
            return "MAC not found"
    else:    
        host = str(request.args.get('host'))
        try:
            macaddr = win_mac(host)
        except Exception, e:
            return str(e)
        return macaddr

@app.route('/update', methods=['GET'])
@authorize
def update():
    try:
        scanner = Scan(config.get('scan','dest'))
        scanner.do()
        saveto(scanner,g.db)
    except Exception, e:
        raise e
        abort(500)
    return redirect(url_for('index'))

# operation
@app.route('/info', methods=['POST'])
@authorize
def info():
    name = request.form['name']
    comment = request.form['comment']
    mac = request.form['mac'].upper()
    if not mac:
        mac = None
    else:
        if not re.match("^([0-9A-F]{2}[-]){5}([0-9A-F]{2})$", mac):
            return "unknow mac address"
    ip = request.form['ip']
    g.db.cur.execute(SQL.update_INFO, (mac, name, comment, ip))
    g.db.commit()
    return redirect(url_for('userip', ip=ip))

@app.route('/clear', methods=['POST'])
@authorize
def clear():
    ip = request.form['ip']
    g.db.cur.execute(SQL.del_INFO, (ip,))
    g.db.commit()
    return redirect(url_for('userip', ip=ip))
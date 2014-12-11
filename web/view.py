#!/usr/bin/env python
# -*- coding:utf-8 -*-
from web import app
from flask import g, request, render_template, abort, session, redirect, url_for,make_response
from db import database
from scanner import win_mac, Scan, ip2int, int2ip
from run import saveto, config
import logging

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
def index():
    sql = "SELECT `ip`,`mac` FROM `%s`  ORDER BY `rowid` ASC" % config.get('scan','netname')
    sql_ip = 'select count(ip) from `%s`' % config.get('scan','netname')
    sql_mac = 'select count(mac) from `%s`' % config.get('scan','netname')
    r = g.db.cur.execute(sql)
    if r:
        info = []
        for row in g.db.cur.fetchall():
            # clear the None value
            row = map(lambda x: x if x else '', row)
            info.append(dict(ip=row[0], mac=row[1]))
        unused = g.db.cur.execute(sql_ip).fetchone()[0]
        used = g.db.cur.execute(sql_mac).fetchone()[0]
        return render_template('index.html', info=info, title=config.get('scan','netname'), used=used, unused=unused)
    else:
        return redirect(url_for('about'))

@app.route('/detail')
@authorize
def detail():
    sql = "SELECT `rowid`,* FROM `%s`  ORDER BY `rowid` ASC" % config.get('scan','netname')
    r = g.db.cur.execute(sql)
    if r:
        info = []
        for row in g.db.cur.fetchall():
            # clear the None value
            row = map(lambda x: x if x else '', row)
            info.append(dict(num=row[0], ip=row[1], mac=row[2], name=row[3], comment=row[4], time=row[5]))
        sql_ip = 'select count(ip) from `%s`' % config.get('scan','netname')
        sql_mac = 'select count(mac) from `%s`' % config.get('scan','netname')
        unused = g.db.cur.execute(sql_ip).fetchone()[0]
        used = g.db.cur.execute(sql_mac).fetchone()[0]
        return render_template('detail.html', info=info, title=config.get('scan','netname'), used=used, unused=unused)
    else:
        return redirect(url_for('about'))

@app.route('/tools')
def tools():
    return render_template('tools.html',title="tools",netname=config.get('scan','netname'))

@app.route('/about')
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
    intip = ip2int(ip)
    lastip = int2ip(intip-1)
    nextip = int2ip(intip+1)
    sql = "SELECT * FROM `%s` WHERE `ip` = ?" % config.get('scan','netname')
    r = g.db.cur.execute(sql, (ip,)).fetchone()
    if r:
        ip, mac, name, comment, time, last = map(lambda x: x if x else '', r)
        return render_template('table.html', ip=ip, mac=mac, name=name, comment=comment, time=time, last=last, lastip=lastip, nextip=nextip, title=ip)
    else:
        return 'not fond!'

# API
# models
@app.route('/get', methods=['GET'])
def getmac():
    host = str(request.args.get('host', ''))
    try:
        macaddr = win_mac(host)
    except Exception, e:
        return str(e)
    return macaddr

@app.route('/update', methods=['GET'])
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
    sql = "UPDATE `%s` SET name=?,comment=? WHERE ip = ?" % config.get('scan','netname')
    name = request.form['name']
    comment = request.form['comment']
    ip = request.form['ip']
    fields = map(lambda x: x if x else '', (name, comment, ip))
    g.db.cur.execute(sql, fields)
    g.db.commit()
    return redirect(url_for('userip', ip=ip))

@app.route('/clear', methods=['POST'])
@authorize
def clear():
    sql = "UPDATE `%s` SET mac=Null,time=Null WHERE ip = ?" % config.get('scan','netname')
    ip = request.form['ip']
    g.db.cur.execute(sql, (ip,))
    g.db.commit()
    return redirect(url_for('userip', ip=ip))
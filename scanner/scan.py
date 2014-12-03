#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os, sys, re, threading, socket, struct
from ipmac import win_mac
#import logging
#logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), level = logging.DEBUG)

def bin8(n):
    return "{0:08b}".format(n)[-8:]

def show8(n):
    return '.'.join([ str(int(n[i:i+8],2)) for i in range(0,32,8) ])

def format32(b):
    return '{:0>32}'.format(b)[0:32]

def inet_aton(ip_string):
    return int(''.join([ bin8(int(b)) for b in ip_string.split('.')]),2)

def inet_ntoa(ip):
    return show8(format32(bin(ip)[2:]))

def ip2int(ip_string):
    return struct.unpack('!I',socket.inet_aton(ip_string))[0]

def int2ip(ip):
    return socket.inet_ntoa(struct.pack('!I',ip))

def ip_compare(a,b):
    # big int num operation will be long type
    return int(inet_aton(a)-inet_aton(b)) 

def ip_sort(a,b):
    # big int num operation will be long type
    return int(ip2int(a)>ip2int(b))

class Scan(object):
    def __init__(self, lan,show=1):
        # super(Scan, self).__init__()
        self.addrs = {}
        ip_s = lan.split('/')[0]
        mask_s = int(lan.split('/')[1])
        ip_b =  ''.join([ bin8(int(b)) for b in ip_s.split('.')])
        mask_b = '{:0<32}'.format(mask_s*'1')[0:32]
        broadcast_mask = '{:0>32}'.format((32-int(mask_s))*'1')[0:32]
        ip = int(ip_b,2)
        mask  = int(mask_b,2)
        broadcast = int(broadcast_mask,2)
        net_id = ip&mask
        broadcast = ip|broadcast
        net_name = inet_ntoa(net_id)
        # show state 1:open 0:close
        self.state = show
        self.net_id = net_id
        self.broadcast = broadcast
        self.netname = "%s/%s" %(net_name,mask_s)
        self.dsts = broadcast-self.net_id-1
        # print("#[DEST] {0}".format(self.netname))
        self.iplist = [ inet_ntoa(x) for x in range(self.net_id+1,self.broadcast)]

    def do(self):
        # platform
        run = self.platform()
        #asynchronous
        threads  = []
        for dst in self.iplist:
            t = threading.Thread(target=run, args=(dst,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        # ip_list =  sorted(self.addrs.keys(),cmp=ip_compare)
        # self.iplist = ip_list
        # filter
        if self.state:
            show = lambda x:self.addrs[x]
        else:
            show = lambda x:not self.addrs[x]
        iplist= filter(show,self.iplist)
        self.info = [ (ip,self.addrs[ip]) for ip in iplist]
        return self.info
        # for ip in show_list:
        #     print("{0}|{1}".format(ip,self.addrs[ip]))
        # print("[GET] {0}/{1}".format(len(show_list),self.dsts))
    def platform(self):
        platform = sys.platform
        if  platform == 'win32':
            return self.winRun
        elif platform == 'darwin':
            return self.osXRun
        else:
            return self.linuxRun
    # must to be improve
    def osXRun(self,ip):
        result = os.popen('ping -c1 -W1 -q %s' %ip).read()
        res = re.search('1 packets received',result)
        if res:
            r = os.popen('arp %s' %ip).read().split()
            try:
                self.addrs[ip] = r[3]
            except IndexError, e:
                self.addrs[ip] = None
        else:
            self.addrs[ip] = None

    def linuxRun(self,ip):
        result = os.popen('ping -c1 -W1 -q %s' % ip).read()
        res = re.search('1 received',result)
        if res:
            mac = os.popen("arp -n %s |awk '/%s/ {print $3}' " %(ip,ip)).read().split('\n')[0]
            self.addrs[ip] = mac
        else:
            self.addrs[ip] = None

    def winRun(self,ip):
        # get the mac address in the LAN
        try:
            mac = win_mac(ip)
        except WindowsError as e:
            mac = None
        self.addrs[ip] = mac
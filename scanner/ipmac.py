#!/usr/bin/env python
#-*- coding:utf-8 -*-
import socket
def get_ipaddress():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("baidu.com",80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception, e:
        return socket.gethostbyname(socket.gethostname())

 
def get_macaddress(host):
    import sys,re
    re = re.compile('linux')
    math = re.search(sys.platform)
    if math:
        import uuid
        return uuid.UUID(int = uuid.getnode()).hex[-12:]
    else:
        return win_mac(host)
    
 
def win_mac(host):
    """ Returns the MAC address of a network host, requires >= WIN2K.
    """
    import ctypes
    import struct
    # Check for api availability
    try:
        SendARP = ctypes.windll.Iphlpapi.SendARP
    except:
        raise NotImplementedError('Usage only on Windows 2000 and above')
 
    # Doesn't work with loopbacks, but let's try and help.
    if host == '127.0.0.1' or host.lower() == 'localhost':
        host = socket.gethostname()
 
    # gethostbyname blocks, so use it wisely.
    try:
        inetaddr = ctypes.windll.wsock32.inet_addr(host)
        if inetaddr in (0, -1):
            raise Exception
    except:
        hostip = socket.gethostbyname(host)
        inetaddr = ctypes.windll.wsock32.inet_addr(hostip)
 
    buffer = ctypes.c_buffer(6)
    addlen = ctypes.c_ulong(ctypes.sizeof(buffer))
    if SendARP(inetaddr, 0, ctypes.byref(buffer), ctypes.byref(addlen)) != 0:
        raise WindowsError('Retreival of mac address(%s) - failed' % host)
 
    # Convert binary data into a string.
    macaddr = []
    for intval in struct.unpack('BBBBBB', buffer):
        if intval > 15:
            replacestr = '0x'
        else:
            replacestr = 'x'
        macaddr.append(hex(intval).replace(replacestr, ''))
    return '-'.join([i.upper() for i in macaddr ])
 
if __name__ == '__main__':
    win_mac('192.168.1.1')
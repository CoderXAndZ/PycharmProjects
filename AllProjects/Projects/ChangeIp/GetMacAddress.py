#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# FileName:ChangeIP.py

import uuid
import socket
import struct
import fcntl

# 获取mac地址
def get_mac_address():
    mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in  range(0,11,2)])

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':
    print(get_mac_address())

    print("获取：",get_ip())

    # print("获取ip地址：",get_ip_address('lo'))
    # print("获取ip地址2：", get_ip_address('eth0'))

    # 获取IP地址和主机名
    pc_name = socket.getfqdn(socket.gethostname())
    print("IP地址:",pc_name)

    # pc_ip = socket.gethostbyname(socket.gethostname())
    # print("主机名：", pc_ip)
    #
    # addrInfo = socket.getaddrinfo(socket.gethostname(),0,socket.AF_INET,socket.SOCK_STREAM)
    # print("地址信息：",addrInfo)




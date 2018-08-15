#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-

import socket

# 创建对象
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 绑定端口和ip
s.bind(('localhost',8122)) # 127.0.0.1 == localhost
# 请求限制
s.listen(8)
while True:
    connection,address = s.accept()
    buf = connection.recv(10)
    connection.send(buf)
s.closed()
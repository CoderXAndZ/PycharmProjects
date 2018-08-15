#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-

# import logging
#
# logger = logging.getLogger()
# hdlr = logging.FileHandler('/Users/admin/Desktop/修改IP/sendlog.txt')
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr)
# logger.setLevel(logging.NOTSET)
#
# logger.debug('this is a bug message')
# logger.error('this is an error message')

# # 常用方法
# d = open('a','r')
# d.read()
# d.close()
#
# # with 语句，不需要调用closed方法：
# # 使用时会去调用
# with open('a','r') as a:
#     content = a.read()

# # with 手动编辑一个让 with 调用的对象
# class sth(object):
#     def __init__(self,name):
#         self.e = name
#     def __enter__(self):
#         print("进入方法")
#         return self.e
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print("退出方法")
#
# with sth('Lisa') as e:
#     print(e)
#
# # as e 中的 e 是 enter 方法返回的对象，如果enter方法不做返回，e 里面是什么都没有的


"""
输出结果：

进入方法
Lisa
退出方法
"""

# class myException(Exception):
#
#     def __init__(self,error,msg):
#         self.error = error
#         self.msg = msg
#         self.args = (error,msg)
#
# try:
#     raise myException(1,'my exception')
# except Exception as e:
#     print(e)


"""
定义一个函数 func(domainlist)
domainlist 为域名列表，例如：['xx.com','www.xx.com','www.xxx.com'...]
函数功能：要求依次 ping 域名，
如果 ping 域名返回结果为：request time out，则把域名记录到日志文件里，
并且跳过继续 ping 下个域名。
提示用 os 模块的相关方法
"""
# import os
#
# input_count = input('please enter a number:')
#
# def ping_url(domainlist, count):
#     # 依次 ping 域名列表中的域名
#     for i in domainlist:
#         os.system('ping -c %s %s' % (count, i))
#
# ping_url(['126.com'], input_count)


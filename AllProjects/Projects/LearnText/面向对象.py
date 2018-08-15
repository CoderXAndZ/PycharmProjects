#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
# FileName:Test1.py

#
# class test(object):
#
#     def __init__(self,var1):
#         self.var1 = var1
#
#     def get(self,a=None):
#         return self.var1
#
#     pass
#
# # 函数 get
# def get(a):
#     return a
#
# """
# t 是类 test 的一个实例
# """
# t = test("测试一下")
# print(t.get())

# print(t.get(4)) # 调用
# print(get(5))  # 调用


# 返回任意链接的网页内容
import  urllib
import logging
def get_content(url):
    if not isinstance(url,str):
        return "输入的网址类型不对"
    if not url.startswith('http://') and not url.startswith('https://'):
        return "error url_format"
    try:
        url_info = urlopen(url).read()
    except Exception as e:
        logging.debug(e)
    else:
        return url_info

import os

# 查找任意磁盘路径下的文件夹列表，没有则返回“Not dir”
def get_dir(f):
    if not os.path.isdir(f):
        return "输入的磁盘路径不正确"

    list_dir = []
    for i in os.listdir(f):
        list_dir.append(i)

    if list_dir:
        return list_dir
    else:
        return "Not dir"


if __name__ == '__main__':
    print(get_content("https://www.baidu.com"))
    # get_content("www.baidu.com")
    #
    # print(get_dir("/Users/admin/Desktop/考核表"))
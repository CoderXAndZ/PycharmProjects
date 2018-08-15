#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-

#
# class test(object):
#
#     a = 8
#
#     def func(self):
#         return self.arg1, self.arg2
#
#     def __init__(self,arg1,arg2):
#         self.arg1 = arg1
#         self.arg2 = arg2
#
#     def __del__(self):
#         del self.arg1
#         del self.arg2
#
# # 调用
#
# t = test(5,6)
# print(t.a)
# print(t.func())

"""
1、func(url,folder_path) 获取url地址的内容，保存到folder_path的文件目录下，并随机生成一个文件名
"""

import urllib
from urllib import request
import random
import os

def save_url_content(url, folder_path=None):
    if not url.startswith("http://") and not url.startswith("https://"):
        return u'url地址不符合规则'

    if not os.path.isdir(folder_path):
        return u'folder_path非文件夹'

    d = urllib.request.urlopen(url)
    content = d.read()

    rand_filename = 'test_%s'%random.randint(1,1000)
    file_path = os.path.join(folder_path,rand_filename)
    d = open(file_path,'w')
    d.write(str(content))
    d.close()
    return file_path

# print(save_url_content("http://www.baidu.com",'/Users/admin/Desktop/修改IP'))

# 定义一个func(url),分析该url内容里有多少个链接
def get_url_count(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return u'url地址不符合规则'

    d = urllib.request.urlopen(url)
    content = d.read()
    href = content.split('<a href='.encode())
    return len(href) - 1

# print(get_url_count("http://www.baidu.com"))

# 定义一个func(folder_path)，合并该目录下所有文件，生成一个all.txt
# 使用递归实现
def merge(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path,file)
        if os.path.isdir(file_path): # 是文件夹
            merge(file_path)
        else:
            merge_file = open('/Users/admin/Desktop/修改IP/text.txt','ab+')
            content = open(file_path,'r').read()
            merge_file.write(content.encode())
            merge_file.close()

# merge("/Users/admin/Desktop/修改IP/获取网页数据")

# 定义一个func(url),获取他？后的参数，并返回成一个dict
from urllib.parse import urlparse

def querys(url):
    qy = urlparse(url).query
    item = urllib.parse.parse_qs(qy).items()
    return dict([(k,v[0]) for k,v in item])

# print(querys("http://123.com")) # {}
print(querys("http://api/bsi?g=6&m=8")) # {'g': '6', 'm': '8'}
# print(querys("http://api/info?in=56")) # {'in': '56'}

#使用递归实现
def delelte(dir_path):
    for path in os.listdir(dir_path):
        file_path = os.path.join(dir_path,path)
        if os.path.isdir(file_path):
            delelte(file_path)
        else:
            os.remove(file_path)

# delelte("/Users/admin/Desktop/修改IP/获取网页数据的副本")


# class Base(object):
#
#     def __init__(self,name):
#         self.name = name
#
# class AClass(Base):
#
#     def get_name(self):
#         return self.name
#
#
# a = AClass("李四")
# print(a.get_name())


#
class boy(object):

    gender = 1
    def __init__(self,name):
        self.name = name

class girl(object):

    gender = 0
    def __init__(self,name):
        self.name = name

class love(object):

    def __init__(self,first,second):
        self.first = first
        self.second = second

    def meet(self):
        return "%s和%s相遇了"%(self.first,self.second)

    def marry(self):
        return "%s和%s结婚了"%(self.first, self.second)

    def children(self):
        return "%s和%s有baby了"%(self.first, self.second)

class normal_love(love):

    def __init__(self,first,second):
        if 1 != (first.gender + second.gender):
            print('对象引入错误')
        else:
            love.__init__(self,first,second)

girl = girl("kk")
boy = boy('oo')
love = normal_love(girl,boy)
print(love.meet())

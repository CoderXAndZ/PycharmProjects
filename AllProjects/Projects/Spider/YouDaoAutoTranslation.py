#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 有道在线翻译爬取并隐藏自身防止ip被拉黑
'''
一是做一下伪装，添加header头，且每隔一段时间进行请求
二是使用代理：
    1.参数是一个字典{'类型':'代理ip:端口号'}
    proxy_support = urllib.request.ProxyHandler({})
    2.定制、创建一个opener
    opener = urllib.request.build_opener(proxy_support)
    3a.安装 opener 到系统中，一劳永逸，在此之后，只要使用urlopen就会自动的使用定制好的opener进行工作
    urllib.request.install_opener(opener)
    3b.调用 opener 如果不想替换掉默认的opener，只是在特殊需要使用
    opener.open(url)
'''

import urllib.request
import urllib.parse
import json
import time
import random
import hashlib #md5 加密

while True:
    content = input("请输入翻译内容：")

    if content == 'q!':
        break

    # 注意：抓取的url http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule  去掉_o
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    """
    header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0"}
    # data = {'type':'AUTO','i':content,'doctype':'json','xmlVersion':'1.6','keyfrom':'fanyi.web','ue':'UTF-8','typoResult':'true'}
    """

    client = 'fanyideskweb'
    salt = str(int(time.time()*1000) + random.randint(1,10)).encode('utf-8')
    c = 'ebSeFb%=XZ%T[KZ)c(sy!'.encode('utf-8')

    md5 = hashlib.md5()
    md5.update(client.encode('utf-8'))
    md5.update(content.encode('utf-8'))
    md5.update(salt)
    md5.update(c)
    sign = md5.hexdigest()

    data = {'action':'FY_BY_CLICKBUTTION',
            'client':client,
            'doctype':'json',
            'from':'AUTO',
            'to':'AUTO',
            'i':content,
            'keyfrom':'fanyi.web',
            'salt':salt,
            'sign':sign,
            'smartresult':'dict',
            'typoResult':'true',
            'version':'2.1'
            }

    data_utf8 = urllib.parse.urlencode(data).encode('utf-8')

    print("data_utf8：",data_utf8)

    request = urllib.request.Request(url,data_utf8) # ,header
    request.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0')

    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')

    target = json.loads(html)
    response.close()
    print("结果：\n",target)
    target = target['translateResult'][0][0]['tgt']
    print("目标值：", target)
    time.sleep(5)
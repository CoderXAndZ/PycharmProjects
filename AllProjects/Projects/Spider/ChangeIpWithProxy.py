#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 替换ip请求网络
'''
国内透明代理IP http://www.xicidaili.com/nt/
快代理 https://www.kuaidaili.com/free/inha/1/
西刺免费代理IP http://www.xicidaili.com
'''

import urllib.request
import random

# 测试目前ip
url = 'http://www.whatismyip.com.tw'

iplist = ['182.90.94.113:53281','119.28.152.208:80','116.226.219.94:9797',]

proxy_support = urllib.request.ProxyHandler({'http':random.choice(iplist)})

opener = urllib.request.build_opener(proxy_support) # 创建
opener.addheaders = [('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0')]
urllib.request.install_opener(opener) # 安装

response = urllib.request.urlopen(url) # 访问
html = response.read().decode('utf-8')

print(html) # 查看切换 IP 是否成功

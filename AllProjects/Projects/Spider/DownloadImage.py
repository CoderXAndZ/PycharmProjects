#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 抓取 妹子图 并存储

import urllib.request
import os
import random

def open_url(url):

    request = urllib.request.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0')
    # 添加代理，改变 ip
    iplist = ['182.90.94.113:53281', '119.28.152.208:80', '116.226.219.94:9797', ]
    proxy_support = urllib.request.ProxyHandler({'http': random.choice(iplist)})
    opener = urllib.request.build_opener(proxy_support)  # 创建
    urllib.request.install_opener(opener)  # 安装

    # 访问网页
    response = urllib.request.urlopen(request)
    html = response.read()
    return html

# 获取图片id
def get_page(url):
    html = open_url(url).decode('utf-8')

    a = html.find('current-comment-page') + 23
    b = html.find(']',a)

    print("图片id是：",html[a:b])

    return html[a:b]

# 根据 url 获取图片添加到数组并返回
def find_imgs(url):
    html = open_url(url).decode('utf-8')
    print("html内容：", html)

    imgs_addrs = []

    a = html.find('img src=')

    while a != -1: # 找到字符串
        print("找到字符串a")
        b = html.find('.gif',a,a+255)
        if b != -1:
            print("找到字符串b")
            imgs_addrs.append(html[a+9:b+4])
        else:
            print("未找到字符串b")
            b = a + 9

        a = html.find('img src=',b)

    return imgs_addrs

# 保存图片
def save_imgs(folder,imgs_addrs):
    print("folder", folder, "imgs_addrs", imgs_addrs)
    for each in imgs_addrs:
        filename = each.split('/')[-1]
        with open(filename,'wb') as f:
            img = open_url(each)
            f.write(img)

# 下载图片
def download_img(folder='Image',pages=10):
    if os.path.exists(folder) == False:
        os.mkdir(folder)
        os.chdir(folder)

    url = 'http://jandan.net/ooxx/'
    page_num = int(get_page(url))

    for i in range(pages):
        page_num -= i
        page_url = url + 'page-' + str(page_num) + '#comments'
        print("页面链接是：",page_url)
        # 图片列表
        imgs_addrs = find_imgs(page_url)
        save_imgs(folder,imgs_addrs)

if __name__ == '__main__':
    download_img()
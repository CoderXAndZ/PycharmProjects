#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 寻找小融


import urllib
from urllib import request,parse
import requests
import time
import hashlib #md5 加密
import json
from selenium import webdriver
from selenium import common
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from datetime import datetime,timedelta # 时间判断
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote import webelement

# 获取寻找小融页面数据
def getFindXiaoRongData(user_id):
    # http: // game.rongtuojinrong.com / bigWheel / findMissRong?
    # url = "http://game.rongtuojinrong.com/bigWheel/findMissRongIndex?"
    url = '%s%s%s' % ("http://game.rongtuojinrong.com/bigWheel/findMissRong?","usrId=",user_id)
    # now_time = round(time.time())
    # token_str = "appid=iOS&user_id=%s&shijian=%d" % (user_id, now_time)
    # hash = hashlib.md5()
    # hash.update(token_str.encode('utf-8'))
    # token_md5 = hash.hexdigest()
    #
    # # 参数
    # params = {
    # 'appid': 'iOS',
    #           'user_id': user_id,
    #           'shijian': now_time,
    #           'token': token_md5,
    #           'defidenshuxing': "1"
    #           }
    # data = parse.urlencode(params)
    print(url)
    opener = request.urlopen(url)
    content = opener.read().decode('utf-8')
    opener.close()

    # 密码自动填充
    wd = webdriver.Firefox()

    try:
        wd.get(url)
        # wd.maximize_window()
        wait = WebDriverWait(wd, timeout=10)
        wait.until(expected_conditions.title_is("小融真的藏不住？"))

        for num in range(0,40):
            time.sleep(0.5)  # 等待 1 秒
            #网页中的代码：<div class="g2_item g2_clicked" style="width: 178.667px; height: 178.667px;"></div>
            wd.find_element_by_css_selector(".g2_item.g2_clicked").click()
            #网页中的代码：<div>过关：<span class="g2_cs">1</span></div>
            text = wd.find_element_by_class_name("g2_cs").text  # 找到“过关的text值”
            print("当前是第" + text + "关")

    except NoSuchElementException as e:
        print("异常信息：", e.msg)

if __name__ == '__main__':

    user_id = input("请输入用户的user_id，点击enter：")
    getFindXiaoRongData(user_id)
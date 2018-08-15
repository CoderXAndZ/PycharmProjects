#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 自动投标

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

global xiangmu_id
global time_begin

# 获取首页数据
def get_bid_data(user_id,money, pwd_str,bid_lilv):
    url = "https://php.rongtuojinrong.com/Rongtuoxinsoc/indexapp/appindexalljava?"
    now_time = round(time.time())
    token_str = "AppId=iOS&UserId=%s&AppTime=%d"%(user_id,now_time)
    # print("now_time:",now_time,"\ntoken_str:",token_str)
    hash = hashlib.md5()
    hash.update(token_str.encode('utf-8'))
    token_md5 = hash.hexdigest()
    # print("hash:", hash, "\ntoken_md5:", token_md5)

    # 参数
    params = {'AppId':'iOS',
              'UserId':user_id,
              'AppTime':now_time,
              'Token':token_md5,
              'defidenshuxing':"1"
              }
    request = requests.post(url,data=params)
    result_dict = json.loads(request.text) # 把 str 转换成 dict
    result_json = json.dumps(result_dict, sort_keys=True, indent=2) # 把 dict 转换成 json
    xiangmu_data = result_dict["data"]["xiangmudate"] # 获取首页项目标数据
    # print(request.encoding) # 查看请求的encoding方式 ISO-8859-1
    # print("请求结果：", request.status_code)
    # print("\n\n请求数据结果request.text：",request.text,"\nrequest.text数据类型：",type(request.text))
    # print("\n\njson结果result：",result_json,"\nresult数据类型：",type(result_json))
    print("项目标数据：",xiangmu_data)

    for xiangmu in xiangmu_data:
        # if float(xiangmu["kaishi"]) > 0: # 新标，未到时间，未开始
        #     # difftime = time.mktime(xiangmu["start_time"]) - round(time.time())
        #     # print("获取时间差：",difftime)
        #     # print("未开始，获取时间差：",xiangmu["start_time"])
        #
        #     # time.sleep(1)
        #     time_judge()
        # else:
        if float(xiangmu["lilv"]) == float(bid_lilv):

            if (float(xiangmu["jindu"])/100 < 1):
                global xiangmu_id
                xiangmu_id = xiangmu["jie_id"]
                print("已经开始，获取时间差：", xiangmu["start_time"])
                struct_time = time.strptime(xiangmu["start_time"],"%Y-%m-%d %H:%M:%S") # start_time --> 2018-02-06 14:52:00 转换成时间数组
                time_stamp =  time.mktime(struct_time) # 时间数组 转换成时间戳
                difftime = time_stamp - round(time.time()) # 时间差
                print("时间差：",difftime,"时间time_stamp：",time_stamp)
                print("正在投，蓝色显示,获取jie_id",xiangmu_id)

                # 确认投资web页
                web_data(user_id, money, pwd_str)
                return
            else:
                print("不能再投")

    print("没有合适利率的标或标的额度已完")

    if request.status_code == 200:
        return (True) # 请求成功！
    else:
        return False # 请求失败！

# 确认投资web页
def web_data(user_id,money,pwd_str):
    url = "https://www.rongtuojinrong.com/hsesb/esb?"
    now_time = round(time.time())
    token_str = "AppId=huiyuan&UserId=%s&AppTime=%d" % (user_id, now_time)
    hash = hashlib.md5()
    hash.update(token_str.encode('utf-8'))
    token_md5 = hash.hexdigest() # 验签失败，检查token的参数和params的参数是否相同

    # 参数
    params = {'AppId': 'huiyuan',
              'UserId': user_id,
              'AppTime': now_time,
              'Token': token_md5,
              'defidenshuxing': "1",
              "CmdId":"LLBidApply",
              "ProjId":xiangmu_id,
              "TransAmt":money,
              "RedPacket":"",
              "InterestCoupon":""
            }
    data = parse.urlencode(params)
    opener = request.urlopen(url+data)
    content = opener.read().decode('utf-8')
    opener.close()
    print("web页结果：",content) # ,"\n\n\njson结果：",json.loads(content)

    print("网址是：",url+data)

    # 密码自动填充
    wd = webdriver.Firefox()

    try:
        wd.get(url + data)
        # wd.maximize_window()
        wait = WebDriverWait(wd, timeout=10)
        wait.until(EC.presence_of_element_located((By.ID,"pass")),message=u"元素加载超时！")
        wait.until(EC.presence_of_element_located((By.ID, "mainAcceptIpt")), message=u"元素加载超时！")
        input = wd.find_element_by_id("pass")
        print("current_url:",wd.current_url)
        input.send_keys(pwd_str) # 密码自动填充
        wd.find_element_by_id('mainAcceptIpt').click()
        # stasus = wd.find_element_by_id('sub').click()

        print("cookies：",wd.get_cookies())

        # print("\n\nwd：",wd,"\n\n\n点击结果：status",stasus)
        print("current_url2:", wd.current_url)
        print("wd.current_window_handle",wd.current_window_handle)

        print("current_url3:", wd.current_url)
        time_end = time.time()
        time_interval = time_end-time_begin
        print("运行所需时间:",time_interval)
        time.sleep(8)
        wd.close() # 关闭浏览器

    except NoSuchElementException as e:
        print("异常信息：",e.msg)

# 时间判断
def time_judge(user_id,money,pwd_str,time_bid,bid_lilv):
    flag = 1
    while flag:
        if datetime.now().strftime('%H:%M:%S') > time_bid:
            print("明天执行")
            tomorrow_day = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d') + time_bid
            while datetime.now().strftime('%H:%M:%S') >= time_bid or datetime.now().strftime('%Y-%m-%d %H-%M-%S') < tomorrow_day:
                pass
            break
        else:
            print("今天执行")
            while datetime.now().strftime('%H:%M:%S') < time_bid:
                pass
            # 获取首页数据
            stasus = get_bid_data(user_id,money,pwd_str,bid_lilv)
            break

if __name__ == '__main__':

    global time_begin
    time_begin = time.time()

    user_id = input("请输入用户的user_id，点击enter：")
    money = input("请输入投标金额，点击enter：")
    pwd_str = input("请输入交易密码，点击enter：")
    time_bid = input("请输入投标时间，格式（14:00:00），点击enter：")
    bid_lilv = input("请输入希望投资的利率，格式（10.0），点击enter：")

    time_judge(user_id,money,pwd_str,time_bid,bid_lilv)

"""
if kaishi > 0：
    新标，未到时间，未开始
else: # 开始

    if jindu / 100 < 1 
        正在投，蓝色显示
        获取jie_id
        获取这些标的预期年化收益，进行从高到低排序
    else：
        if zhuangtai == 4：
            满标=已售罄
        elif zhuangtai ==6:
            还款中=收益中
        elif zhuangtai ==8:
            还款完成=已结清
        else zhuangtai == 10: 
            没有可投，已经满标，但是还未变成灰色
"""




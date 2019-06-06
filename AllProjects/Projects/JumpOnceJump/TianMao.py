# -*- coding: utf-8 -*-

import time
import random
import json
from PIL import Image, ImageDraw
import wda

import math
import numpy as np
import cv2


#开启HTTP请求与回应的LOG
# wda.DEBUG = True
c = wda.Client('http://localhost:8100')
# c = wda.Client()
s = c.session()  # 'com.taobao.taobao4iphone'

# 打印客户端状态
print(c.status())

# # 等待客户端启动准备
# c.wait_ready(timeout=300)  # 等待300s，默认120s
# # 检查可用性
# c.healthcheck()


# 获取屏幕截图
def pull_screenshot():
    c.screenshot('screen.png')


# 点击跳转
def jump(distance):
    # 1 是 1s
    s.tap_hold(random.uniform(0, 320), random.uniform(64, 320), 1)


# 逛店50次领喵币
def get_miao_bi():

    for num in range(0, 50):
        print("------- 第", num, "次逛店 -------")

        # 点击 '领喵币' x:307~378.5  y:576~650.5
        s.click(343, 615)
        print("-----------领喵币-----------")
        time.sleep(1)
        # 查找'去逛店'，点击
        s.click(333, 484)
        print("-----------去逛店-----------")

        # 页面等10s, 多等了2秒，避免加载不出来的情况
        print("-----------正在等待10s-----------")
        time.sleep(12)
        # 猫猫出现了，点击得喵币 339, 367   740 803
        if s(name='猫猫出现啦', className='StaticText').exists:
            s.click(370, 401)
            print("-----------猫猫出现了，点击得喵币-----------")
        elif s(name='明天继续找猫猫', className='StaticText').exists is True:
            # 点击返回 8, 44 [Button]-返回 有可能是左上角的返回，有可能是是右上角的❎号 377,70
            if s(name='返回', className='Other').exists:  # 是否是右上角❎号
                s(name='返回').get().tap()
            else:
                s.click(8, 44)  # 左上角返回
            print("-----------返回-----------")
            break
        else:
            c.screenshot('waiting.png')
            print("-----------出现未知错误，直接返回-----------")
            # 返回 - 是否是右上角❎号
            if s(name='返回', className='Other').exists:
                s(name='返回').get().tap()
            else:
                s.click(8, 44)  # 左上角返回
            return  # 开启下次循环
        time.sleep(2)
        # 点击开心收下
        s.click(172, 579)
        print("-----------开心收下-----------")
        time.sleep(2)
        # 点击返回 8, 44 [Button]-返回 有可能是左上角的返回，有可能是是右上角的❎号 377,70
        if s(name='返回', className='Other').exists:  # 是否是右上角❎号
            s(name='返回').get().tap()
        else:
            s.click(8, 44)   # 左上角返回
        print("-----------返回-----------")
        time.sleep(2)


# 浏览主会场领喵币, 3次机会
def browse_main_venue():

    for num in (0, 3):
        print("------- 第", num, "次浏览主会场 -------")
        # 点击 '领喵币' x:307~378.5  y:576~650.5
        s.click(343, 615)
        print("-----------领喵币-----------")
        time.sleep(1)
        # 去浏览
        # if s(name='去浏览', className='Link').exists:
        #     s(name='去浏览').get().tap()
        # 查找'去浏览'，点击
        s.click(333, 556)
        print("-----------去浏览主会场-----------")
        time.sleep(12)  # 12s后返回即可
        # 猫猫出现了，点击得喵币 339, 367   740 803
        if s(name='猫猫出现啦', className='StaticText').exists:
            # 页面等10s, 多等了2秒，避免加载不出来的情况
            print("-----------正在等待10s-----------")
            time.sleep(11)
            s.click(370, 401)
            print("-----------猫猫出现了，点击得喵币-----------")
            time.sleep(2)
            # 点击开心收下
            s.click(172, 579)
            print("-----------开心收下-----------")
            time.sleep(2)
        # 点击返回 8, 44
        s.click(8, 44)  # 左上角返回
        print("-----------返回-----------")


if __name__ == '__main__':
    pull_screenshot()

    # 逛店50次领喵币
    get_miao_bi()
    print("------- 已经获取50次了, 开始浏览会场 -------")
    # 浏览主会场领喵币, 3次机会
    browse_main_venue()
    print("------- 浏览主会场领喵币结束 -------")

    # 去浏览主播，3次，每次10s


    # # 匹配领喵币模板
    # temp_end = cv2.imread('getMiaoBi.png', 0)
    # print("------喵币：", temp_end)
    # temp_screen = cv2.imread('screen.png', 0)
    # print("------截屏：", temp_screen)
    # # 对比领喵币和截图，如果有领喵币，则点击
    # res_end = cv2.matchTemplate(temp_screen, temp_end, cv2.TM_CCOEFF_NORMED)
    # print(cv2.minMaxLoc(res_end)[1])

    # time.sleep(2)

    # if cv2.minMaxLoc(res_end)[1] == 1:
    #     s.tap(687, 1229)

    # if cv2.minMaxLoc(res_end)[1] > 0.95:
    #     print('未匹配到!')
    #     cv2.imwrite('Resault.png', temp_screen)


    # 打开淘宝
    # taobao_file = s(cl)
    #    s(text=u'发现',className='Button').tap()
    # im = cv2.imread('screen.png', 0)  # 获取图片

    # 淘宝的点击右上角的
    # s.tap(326,45)
#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 自动测试'融托金融'脚本编写

import atx
import time
import wda

client = wda.Client()

def main():
    with client.session('com.ios.rongtuo') as s:
        # 登录
        if s(name = u'登陆其他账户').exists: # 如果存在，切换账户
            s(name = u'登陆其他账户').tap()
            # 输入 用户名 和 密码，点击‘登录’
            s(type='TextField').send_keys('13691457296'+'\n') # .set_text('13691457296'+'\n')
            s(type='SecureTextField').set_text('123789' + '\n')
            s(name=u'登录').tap() # 0 1 5 8
            if s(classname='Other'):
                s(classname='Other', index=0).tap()
                s(classname='Other', index=1).tap()
                s(classname='Other', index=5).tap()
                s(classname='Other', index=8).tap()
        else:
            # 点击 ‘我的’进行‘登录’
            # if s(classname='TabBar').exists:
            s(className = 'Button',index = 3,name='').tap()
            # 输入 用户名 和 密码，点击‘登录’
            s(type='TextField').set_text('13691457296' + '\n')
            s(type='SecureTextField').set_text('123789' + '\n')
            s(name=u'登录').tap()  # 0 1 5 8
            if s(classname='Other'):
                s(classname='Other', index=0).tap()
                s(classname='Other', index=1).tap()
                s(classname='Other', index=5).tap()
                s(classname='Other', index=8).tap()
            # else:
            #     print("没找到‘我的’")


if __name__ == '__main__':
    main()

# d = atx.connect('http://localhost:8100')
# d.start_app("com.ios.rongtuo")
# d(text=u'登陆其他账户').click()
# d(text=u'开始计时').click()
# d(text=u'取消').click()
# d.stop_app()
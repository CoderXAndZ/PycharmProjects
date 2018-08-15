#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 自动打开手机计时器

import time
import atx

# 打开iPhone自带的计时器,开始然后退出
# http://localhost:8100/inspector
# http://localhost:8100/status
d = atx.connect("http://localhost:8100")
d.start_app("com.apple.mobiletimer") # com.ios.rongtuo
d(text=u'计时器').click()
d(text=u'开始计时').click()
d(text=u'取消').click()
d.stop_app()


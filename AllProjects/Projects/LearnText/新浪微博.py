#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-

from weibopy import WeiboOauth2,WeiboClient
import time
import json # json输出格式化
from requests_toolbelt.multipart.encoder import MultipartEncoder

#获取授权码
def get_code():
    APP_KEY = '2162967619' # app key
    APP_SECRET = 'e0b59fdea47020725e0491f1b86ce13a' # app secret
    CALLBACK_URL = 'http://baidu.com' # callback url
    client = WeiboOauth2(APP_KEY, APP_SECRET, CALLBACK_URL)
    url = client.authorize_url
    print(url) # https://api.weibo.com/oauth2/authorize?client_id=2162967619&redirect_uri=http%3A%2F%2Fbaidu.com
    # 回调 code # https://www.baidu.com/?code=d2fff176d2b66a6b736f226fce10f658

    code = "d2fff176d2b66a6b736f226fce10f658"

    request = client.auth_access(code)
    print(request) # {'access_token': '2.004jcLBHVga43C200e107f4c00TUIZ', 'remind_in': '157679999', 'expires_in': 157679999, 'uid': '6430476653', 'isRealName': 'true'}

# 获取微博内容
def get_tweets(access_token):

    begin_time = time.time()

    client = WeiboClient(access_token)

    request = client.get(suffix="statuses/public_timeline.json")
    jsonData = json.dumps(request, sort_keys=True, indent=2) #json输出格式化
    print(request,"\n\n\n",jsonData)
    print("获取微博内容花费时间：",time.time() - begin_time)

# 发送微博，带图片 pic
def post_tweet(access_token):
    client = WeiboClient(access_token)
    files = {'pic':open('水墨荷花.png', 'rb')}
    result = client.post("statuses/share.json",data={"status":"测试一下，看看发送成功了嘛"},files=files)
    print("发送结果：",result)
    files.close()

if __name__ == '__main__':

    # get_code()

    access_token = "2.004jcLBHVga43C200e107f4c00TUIZ"
    get_tweets(access_token) # 获取微博内容

    # post_tweet(access_token)  # 发送微博，带图片 pic
#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 接口测试

import urllib
from urllib import request,parse
from urllib.parse import urlparse # 定义一个func(url),获取他？后的参数，并返回成一个dict
import threading # 多线程
import requests
import time
import hashlib # md5 加密
import json
from json import JSONDecodeError
import logging # 异常数据
import xlwt # 表格创建
from datetime import datetime,timedelta # 时间判断
# import ThreadGetResult # 返回结果的多线程
import threading

www_time_arr = [] # www请求时间数组
php_time_arr = [] # php请求时间数组

# www 获取数据
def get_www_data(url,params):
    time_begin = time.time()
    request = requests.post(url,data=params)
    try:
        global www_time_arr
        result_dict = json.loads(request.text) # 把 str 转换成 dict
        result_json = json.dumps(result_dict, sort_keys=True, indent=2) # 把 dict 转换成 json
        time_consume = time.time() - time_begin
        print("\nwww json结果result：",result_json,"\nwww result数据类型：",type(result_json),"请求所需时间：",time_consume)
        www_time_arr.append(time_consume)
        print("www_time_arr的长度：%d" % len(www_time_arr))
        return (result_json,time_consume)
    except JSONDecodeError as e:
        print("异常信息：", e.msg)

# php 获取数据
def get_php_data(url,params):
    time_begin = time.time()
    request = requests.post(url,data=params)
    try:
        global php_time_arr
        result_dict = json.loads(request.text) # 把 str 转换成 dict
        result_json = json.dumps(result_dict, sort_keys=True, indent=2) # 把 dict 转换成 json
        time_consume = time.time()-time_begin # 耗时计算
        print("\nphp json结果result：",result_json,"\nphp result数据类型：",type(result_json),"请求所需时间：",time_consume)
        php_time_arr.append(time_consume)
        print("php_time_arr的长度：%d"%len(php_time_arr))
        return (result_json,time_consume)
    except JSONDecodeError as e:
        print("异常信息：",e.msg)

# 根据 url 返回参数
def querys_params(url):
    qy = urlparse(url).query
    item = urllib.parse.parse_qs(qy).items()
    return dict([(k, v[0]) for k, v in item])

# 时间判断
def time_judge(time_bid,user_id):
    flag = 1
    while flag:
        if datetime.now().strftime('%H:%M:%S') > time_bid:
            print("明天执行")
            tomorrow_day = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d') + time_bid
            while datetime.now().strftime('%H:%M:%S') >= time_bid or datetime.now().strftime(
                    '%Y-%m-%d %H-%M-%S') < tomorrow_day:
                pass
            break
        else:
            print("今天执行")
            while datetime.now().strftime('%H:%M:%S') < time_bid:
                pass
            # 每个请求 10 次
            start_request_ten(user_id)
            break

# 设置单元格样式
def set_style(name='Arial', height=300, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6

    style.font = font
    # style.borders = borders

    return style

# 创建表格
def create_Excel(rows,columns,url_array):
    # 创建工作簿
    excel = xlwt.Workbook(encoding='utf-8')
    # 创建工作表
    excel_sheet = excel.add_sheet(u'工作表1')
    # 设置每个单元格的宽高
    excel_sheet.col(0).width = (100 * 70)
    excel_sheet.col(1).width = (80 * 70)
    excel_sheet.col(2).width = (80 * 70)
    excel_sheet.col(3).width = (100 * 70)
    excel_sheet.col(4).width = (80 * 70)

    row0 = [u'时间',u'PHP耗时',u'WWW耗时',u'耗时降低率',u'接口']

    date = datetime.now().strftime('%Y-%m-%d %H.%M.%S')

    # 写表头
    for i in range(0,len(row0)):
        excel_sheet.write(0, i, row0[i], set_style('Times New Roman', 400, True))
        # print("第一行，第%d列的值为：" % i, row0[i])

    # 填充数据
    for i in range(0,len(rows)): # 控制行
        for j in range(0, len(row0)): # 控制列
            if j == 0: # 时间
                excel_sheet.write(i+1, j, '%s'%date, set_style())
            elif j == 1: # PHP耗时
                excel_sheet.write(i+1, j, rows[i], set_style())
            elif j == 2: # WWW耗时
                excel_sheet.write(i+1, j, columns[i], set_style())
            elif j == 3: # 接口提升
                excel_sheet.write(i+1, j, (columns[i] - rows[i]) / columns[i] * 100, set_style())
            else:
                excel_sheet.write(i+1, j, url_array[i], set_style())
        print("\n第%d行的值为："%(i+1),'%s'%date, rows[i], columns[i],(columns[i] - rows[i]) / columns[i] * 100,url_array[i])

    excel.save('/Users/admin/Desktop/接口测试结果统计/统计结果 %s.xls'%date)

# 开始请求数据，每个接口 10 次
def start_request_ten(userId):
    php = "https://php.rongtuojinrong.com/rongtuoxinsoc/huishang?"
    www = "https://www.rongtuojinrong.com/hsesb/esb?"

    url_array = [  # 0 回款计划  ---  投资
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=MonthRecivesCashPlan&UserId=12154&Token=a4cdb2347d4f3ae25d0597e86a4b6204&defidenshuxing=1&platformiOS=iOS&AppTime=1523245813&FlagChnl=1&Month=2018-04&AppId=iOS",
        # 1 回款计划-月度查看详情   ----  投资
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=ReciveMoneyMonthDayDetail&platformiOS=iOS&PageNum=1&MonthDay=2018-04&UserId=12154&AppTime=1523245973&FlagChnl=1&defidenshuxing=1&leixing=1&AppId=iOS&Type=1&PageSize=10&Token=f6589271286b9ed2eb7c398f5416caad",
        # 2 回款计划 - 某天的详情 ----  投资
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=DayRecivesCashPlan&Token=cff4876ce116f206a166c125a66f0af4&UserId=12154&defidenshuxing=1&platformiOS=iOS&FlagChnl=1&AppTime=1523251115&AppId=iOS&SearchDate=2018-04-02",
        # 3 月度总览  ----  投资
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=ReciveMoneyMonthlyOverview&Token=0366fd0f7198372945b24a04d7aa9f7c&UserId=12154&defidenshuxing=1&platformiOS=iOS&PageNum=1&Type=1&PageSize=10&AppTime=1523250892&AppId=iOS",
        # 4 绑定银行卡界面  --- 获取推荐银行接口
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLBankOfCommend&UserId=126&Token=8eb6935e8367e113ee081fc9a62df157&defidenshuxing=1&platformiOS=iOS&CmdId=LLBankOfCommend&FlagChnl=1&AppTime=1523252717&AppId=iOS",
        # 5 绑定银行卡界面  --- 判断用户是否开立电子账号
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLQueryIsRegist&UserId=126&Token=02e9e11ae3fb9b890fde08ba3ed5323b&defidenshuxing=1&platformiOS=iOS&CmdId=LLQueryIsRegist&FlagChnl=1&AppTime=1523253022&AppId=iOS",
        # 6 绑定银行卡界面  --- 签约支付(绑卡界面签约接口)
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=Signcreatebill&CardNo=1111111111111111111&platformiOS=iOS&CmdId=Signcreatebill&UserId=126&AppTime=1523253022&BindMob=18953166668&FlagChnl=1&defidenshuxing=1&AppId=iOS&Token=02e9e11ae3fb9b890fde08ba3ed5323b&IdNo=371502198801134027&AcctName=周润秋",
        # 7 绑定银行卡界面  --- 电子账户开立接口
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=RegistAcctNo&BindCardNo=1111111111111111111&platformiOS=iOS&UserId=126&AppTime=1523253022&Mobile=18953166668&FlagChnl=1&defidenshuxing=1&AppId=iOS&Token=02e9e11ae3fb9b890fde08ba3ed5323b&IdNo=371502198801134027&SurName=周润秋",
        # 8 绑定银行卡界面  --- 需要绑卡绑定电子账户
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=SignCard&SigCard=1111111111111111111&platformiOS=iOS&UserId=126&AppTime=1523253022&Mobile=18953166668&FlagChnl=1&defidenshuxing=1&AppId=iOS&Token=02e9e11ae3fb9b890fde08ba3ed5323b",
        # 9 银行卡列表界面 ---- 解卡接口
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=SignCardCancel&UserId=2513&Token=fa0d06450bafb366ad050429281203c3&defidenshuxing=0&platformiOS=iOS&FlagChnl=1&AppTime=1523253834&AppId=iOS&SigCard=1111111111111111111",
        # 10 获取验证码接口 
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=IdentifyCodeSend&UserId=2513&TransType=1&Token=fdd33272a809318e5b8c4a0691c5b68b&defidenshuxing=0&platformiOS=iOS&FlagChnl=1&AppTime=1523254954&AppId=iOS&PhoneNum=15169013960",
        # 11 验证验证码接口
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=IdentifyCodeCheck&UserId=14973&TransType=1&Code=107066&Token=51c5ca5393002fa0b88924ce5dbd68b1&defidenshuxing=1&platformiOS=iOS&CmdId=IdentifyCodeCheck&AppTime=1523255116&AppId=iOS&PhoneNum=15169013960",
        # 12 申请更换手机号界面（获取用户状态的接口，用户之前可能也申请过修改手机号
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=UserInfoReviewStatus&UserId=14973&Token=dc455796e54a783a9e64ed9c363d51bd&defidenshuxing=1&platformiOS=iOS&CmdId=UserInfoReviewStatus&AppTime=1523255223&AppId=iOS",
        # 13 获取我的银行卡列表数据
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLQueryCard&UserId=10719&Token=4eac92a9b31420484683cca14fb9c5c8&defidenshuxing=1&platformiOS=iOS&AppTime=1523250517&FlagChnl=1&AppId=iOS",
        # 14 充值页面 获取充值数据
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiLLQueryEBankAcct&UserId=10719&Token=a8866e02cae1a696673a361adc746a6e&defidenshuxing=1&platformiOS=iOS&CmdId=BendiLLQueryEBankAcct&AppTime=1523251579&FlagChnl=1&AppId=iOS",
        # 15 充值 -- 支付创单
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLNetSave&UserId=10719&Token=4aed492d25da2ad64510d9c85d33d822&defidenshuxing=1&TransAmt=1000.00&platformiOS=iOS&CmdId=LLNetSave&AppTime=1523251666&FlagChnl=1&AppId=iOS",
        # 16 我的首页—融托投资账户金额数据请求
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiGetUserInfo&Token=8339b8b53bc6cc2affd832b271831be6&UserId=11115&AppId=iOS&platformiOS=iOS&AppTime=1523245064&defidenshuxing=1",
        # 17 是否设置交易密码
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=QueryAcctPasswordIsSet&Token=42f36390327b8537162de0d64a39c95c&UserId=194&AppId=iOS&platformiOS=iOS&AppTime=1523245632&defidenshuxing=1&FlagChnl=1",
        # 18 提现列表
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiLLCashQuery&UserId=11115&Token=0685013cd73f9710bb7cc10c1e550031&defidenshuxing=1&platformiOS=iOS&AppTime=1523252179&FlagChnl=1&AppId=iOS",
        # 19 提现开户行省份
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLGetProvince&UserId=194&Token=1d92f641df807f05af10a2cf809d9343&defidenshuxing=1&platformiOS=iOS&AppTime=1523252887&FlagChnl=1&AppId=iOS",
        # 20 提现开户行所在市
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLGetCity&UserId=194&defidenshuxing=1&Token=03f08ed2c11467e3f8f35f2b6596cd2e&Code=34&platformiOS=iOS&AppTime=1523252936&FlagChnl=1&AppId=iOS",
        # 21 提现开户行列表
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=Prcptcdquery&CardNo=6222081602005990337&UserId=194&defidenshuxing=1&Token=e3b2e9d092aaa115e1c1d08564202a43&platformiOS=iOS&CityCode=150500&AppTime=1523253017&FlagChnl=1&AppId=iOS",
        # 22 融托账户—我的债权（//项目状态jkzhuangtai（0：全部，6：未到期，8：已到期，10：冻结中））
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetMyZhaiQuan&UserId=12154&page_size=10&Token=48ee78f4cd49e230ebd10e69d6d2753d&defidenshuxing=1&platformiOS=iOS&txlx=0&jkzhuangtai=0&AppTime=1523253425&xmlx=0&page=1&AppId=iOS",
        # 23 账单-请求有月份数据的接口
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiGetDealMonthList&Token=47df4980cf8ed9602d933ba741f2e86f&UserId=12154&defidenshuxing=1&platformiOS=iOS&PageNum=1&AppTime=1523254322&DealTrench=0,1,2,3,4,5&AppId=iOS",
        # 24 账单-请求选中单独月份内的数据
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiGetDealDetailList&UserId=12154&Token=19ad4bd5944a6ba99d17ac28004ac1e8&defidenshuxing=1&platformiOS=iOS&TransMonth=2018-04&AppTime=1523254323&DealTrench=0,1,2,3,4,5&AppId=iOS",
        # 25 月账单
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiGetMonthDealStats&Token=fad38dfd71ef1eca604fd63563dd48e1&UserId=12154&defidenshuxing=1&platformiOS=iOS&AppTime=1523254748&SearchMonth=2017-12&AppId=iOS",
        # 26 交易密码设置-验证验证码
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=IdentifyCodeCheck&AppId=iOS&UserId=11115&AppTime=1523255371&Token=715b83536a71aa461ac9050306318943&FlagChnl=1&TransType=2&PhoneNum=13520227421&Code=973816&platformiOS=iOS&defidenshuxing=1",
        # 27 项目信息页 数据
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetProjectInfo&Token=1c4aff423a149fb42c54d5cf22b070a0&UserId=9166&jie_id=3116&defidenshuxing=1&platformiOS=iOS&AppTime=1523254471&AppId=iOS",
        # 28 项目列表
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetAllProjectList&UserId=9166&pro_status=0&Token=c7a0d0516357288d37342abf9d037485&defidenshuxing=1&platformiOS=iOS&CmdId=GetAllProjectList&AppTime=1523254929&page=1&AppId=iOS&page_size=6",
        # 29 首页-悬浮米袋
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLPurseDisplay&Token=df987f0c7c37eb9dac3c79e59ac6b1a1&UserId=9166&AppId=iOS&platformiOS=iOS&AppTime=1523255010&defidenshuxing=1",
        # 30 确认投资-可用余额
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=mybalannumbendi&Token=22f6c196da8b58922c444ae76ad90db2&UserId=578&AppId=iOS&platformiOS=iOS&AppTime=1523257743&defidenshuxing=1",
        # 31 确认投资
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLBidApply&AppTime=1523258224&AppId=huiyuan&UserId=578&Token=b889db0da990b9f04d8df1c5500438b9&ProjId=1587&TransAmt=100.00&RedPacket=&InterestCoupon=",
        # 32 我的邀请（邀请过好友的）
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetInviterStats&Token=afb9ac2f34f9a7a2270802f2ae071d08&UserId=12154&AppId=iOS&platformiOS=iOS&AppTime=1523245389&defidenshuxing=1",
        # 33 奖励明细
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetInviterAwardList&AwardType=0&StartTime=1388505600&UserId=12154&Token=77f67545004d49852a15b4a210ae0e31&defidenshuxing=1&PageNum=1&platformiOS=iOS&AppTime=1523245556&EndTime=1523203200&AppId=iOS",
        # 34 我的卡券  -- 已使用和过期体验金
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetExperienceCoupon&Token=976ffd396a1e70215b13a642d9aebd2d&UserId=12154&Status=1,2&defidenshuxing=1&platformiOS=iOS&PageNum=1&AppTime=1523251394&AppId=iOS",
        # 35 绑定银行卡界面 ---- 解卡后绑卡接口
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BindCard&SigCard=1111111111111111111&platformiOS=iOS&UserId=126&AppTime=1523253022&Mobile=18953166668&FlagChnl=1&defidenshuxing=1&AppId=iOS&Token=02e9e11ae3fb9b890fde08ba3ed5323b",
        # 36 风险评估问卷
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetTest&Token=215f3496285fa4eeead4b87e87b7b23a&UserId=10719&defidenshuxing=1&platformiOS=iOS&TestCode=RiskAssessmentQuestionnaire&AppTime=1523250706&AppId=iOS",
        # 37 我的首页—获取用户评级（去评估）
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetUserGradeInfo&UserId=11115&Token=8339b8b53bc6cc2affd832b271831be6&defidenshuxing=1&platformiOS=iOS&CmdId=GetUserGradeInfo&AppTime=1523245064&AppId=iOS",
        # 38 融托投资账户单独金额数据请求
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiGetUserInfodandu&Token=33b9334d8775b481f7e93b5c570b7198&UserId=194&AppId=iOS&platformiOS=iOS&AppTime=1523251036&defidenshuxing=1",
        # 39 项目信息页用于请求num字段判断加息行是否显示
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetInterestCouponNum&Token=f83c0ec6eebd175178108b7e54aad5ad&UserId=9166&ProjId=3116&defidenshuxing=1&platformiOS=iOS&AppTime=1523254436&AppId=iOS",
        # 40 项目-下拉列表
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=XingMuListCategory&UserId=9166&Token=f8d2fefcbe3127c6ad5b7714398f389c&defidenshuxing=1&platformiOS=iOS&CmdId=XingMuListCategory&AppTime=1523255004&AppId=iOS"
    ]

    now_time = round(time.time())

    www_average_time_arr = [] # www 平均请求时间数组
    php_average_time_arr = [] # php 平均请求时间数组

    ts_www = []
    ts_php = []

    for i in range(len(url_array)):

        params = querys_params(url_array[i])
        params['AppTime'] = now_time
        user_id = params['UserId']
        if len(userId) != 0:
            user_id = userId
            params['UserId'] = user_id
        token_str = "AppId=iOS&UserId=%s&AppTime=%d" % (user_id, now_time)
        hash = hashlib.md5()
        hash.update(token_str.encode('utf-8'))
        token_md5 = hash.hexdigest()
        params['Token'] = token_md5
        print("Token：",token_md5,"user_id：",user_id,"token_str：",token_str)
        print("\n第%d个字典值:" % i, params)

        for j in range(0,10):
            thread_www = threading.Thread(target=get_www_data,args=(www, params))
            thread_www.start()
            print("www 当前线程个数：%d" % threading.active_count(), "当前线程：", threading.current_thread())
            ts_www.append(thread_www)

            thread_php = threading.Thread(target=get_php_data, args=(php, params))
            thread_php.start()
            print("php 当前线程个数：%d" % threading.active_count(), "当前线程：", threading.current_thread())
            ts_php.append(thread_php)

        for m in range(0,len(ts_php)):
            ts_www[m].join()
            ts_php[m].join()

    www_total = 0.0  # www 10次总时长
    q = 0
    k = 9
    for q in range(q,len(www_time_arr)):
        www_total += www_time_arr[q]
        if q == k:
            www_average = www_total / 10.0 # www 10次平均值
            www_average_time_arr.append(www_average)
            q = k
            k = k + 10
            www_total = 0.0
    print("www q的值：%d"%q,"\nwww_average_time_arr:",www_average_time_arr,"\nk的值：%d"%k)

    php_total = 0.0  # php 10次总时长
    r = 0
    h = 9
    for r in range(r,len(php_time_arr)):
        php_total += php_time_arr[r]
        if r == h:
            php_average = php_total / 10.0  # php 10次平均值
            php_average_time_arr.append(php_average)
            r = h
            h = h + 10
            php_total = 0.0
    print("php r的值：%d" % r, "\nphp_average_time_arr:", php_average_time_arr, "\nh的值：%d" % h)

    # print("php总时间：%d" % php_total, "www总时间：%d" % www_total)

    print("www请求时间数组：",www_time_arr,"\nwww数组长度：%d"%len(www_time_arr))
    print("php请求时间数组：",php_time_arr,"\nphp数组长度：%d"%len(php_time_arr))

    print("www平均请求时间数组：", www_average_time_arr, "\n www数组长度：%d" % len(www_average_time_arr))
    print("php平均请求时间数组：", php_average_time_arr, "\nphp数组长度：%d" % len(php_average_time_arr))
    print("\n程序共用时：",time.time()-now_time)
    # 创建列表
    create_Excel(php_average_time_arr,www_average_time_arr,url_array)

# 开始请求数据，每个接口 1 次
def start_request_once():
    php = "https://php.rongtuojinrong.com/rongtuoxinsoc/huishang?"
    www = "https://www.rongtuojinrong.com/hsesb/esb?"

    url_array = [  # 0 回款计划  ---  投资
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=MonthRecivesCashPlan&UserId=12154&Token=a4cdb2347d4f3ae25d0597e86a4b6204&defidenshuxing=1&platformiOS=iOS&AppTime=1523245813&FlagChnl=1&Month=2018-04&AppId=iOS",
        # 1 回款计划-月度查看详情   ----  投资
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=ReciveMoneyMonthDayDetail&platformiOS=iOS&PageNum=1&MonthDay=2018-04&UserId=12154&AppTime=1523245973&FlagChnl=1&defidenshuxing=1&leixing=1&AppId=iOS&Type=1&PageSize=10&Token=f6589271286b9ed2eb7c398f5416caad",
        # 2 回款计划 - 某天的详情 ----  投资
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=DayRecivesCashPlan&Token=cff4876ce116f206a166c125a66f0af4&UserId=12154&defidenshuxing=1&platformiOS=iOS&FlagChnl=1&AppTime=1523251115&AppId=iOS&SearchDate=2018-04-02",
        # 3 月度总览  ----  投资
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=ReciveMoneyMonthlyOverview&Token=0366fd0f7198372945b24a04d7aa9f7c&UserId=12154&defidenshuxing=1&platformiOS=iOS&PageNum=1&Type=1&PageSize=10&AppTime=1523250892&AppId=iOS",
        # 4 绑定银行卡界面  --- 获取推荐银行接口
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLBankOfCommend&UserId=126&Token=8eb6935e8367e113ee081fc9a62df157&defidenshuxing=1&platformiOS=iOS&CmdId=LLBankOfCommend&FlagChnl=1&AppTime=1523252717&AppId=iOS",
        # 5 绑定银行卡界面  --- 判断用户是否开立电子账号
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLQueryIsRegist&UserId=126&Token=02e9e11ae3fb9b890fde08ba3ed5323b&defidenshuxing=1&platformiOS=iOS&CmdId=LLQueryIsRegist&FlagChnl=1&AppTime=1523253022&AppId=iOS",
        # 6 绑定银行卡界面  --- 签约支付(绑卡界面签约接口)
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=Signcreatebill&CardNo=1111111111111111111&platformiOS=iOS&CmdId=Signcreatebill&UserId=126&AppTime=1523253022&BindMob=18953166668&FlagChnl=1&defidenshuxing=1&AppId=iOS&Token=02e9e11ae3fb9b890fde08ba3ed5323b&IdNo=371502198801134027&AcctName=周润秋",
        # 7 绑定银行卡界面  --- 需要绑卡绑定电子账户
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=SignCard&SigCard=1111111111111111111&platformiOS=iOS&UserId=126&AppTime=1523253022&Mobile=18953166668&FlagChnl=1&defidenshuxing=1&AppId=iOS&Token=02e9e11ae3fb9b890fde08ba3ed5323b",
        # 8 银行卡列表界面 ---- 解卡接口
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=SignCardCancel&UserId=2513&Token=fa0d06450bafb366ad050429281203c3&defidenshuxing=0&platformiOS=iOS&FlagChnl=1&AppTime=1523253834&AppId=iOS&SigCard=1111111111111111111",
        # # 9 获取验证码接口 
        # "https://www.rongtuojinrong.com/hsesb/esb?CmdId=IdentifyCodeSend&UserId=2513&TransType=1&Token=fdd33272a809318e5b8c4a0691c5b68b&defidenshuxing=0&platformiOS=iOS&FlagChnl=1&AppTime=1523254954&AppId=iOS&PhoneNum=15169013960",
        # 10 验证验证码接口
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=IdentifyCodeCheck&UserId=14973&TransType=1&Code=107066&Token=51c5ca5393002fa0b88924ce5dbd68b1&defidenshuxing=1&platformiOS=iOS&CmdId=IdentifyCodeCheck&AppTime=1523255116&AppId=iOS&PhoneNum=15169013960",
        # 11 申请更换手机号界面（获取用户状态的接口，用户之前可能也申请过修改手机号
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=UserInfoReviewStatus&UserId=14973&Token=dc455796e54a783a9e64ed9c363d51bd&defidenshuxing=1&platformiOS=iOS&CmdId=UserInfoReviewStatus&AppTime=1523255223&AppId=iOS",
        # 12 获取我的银行卡列表数据
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLQueryCard&UserId=10719&Token=4eac92a9b31420484683cca14fb9c5c8&defidenshuxing=1&platformiOS=iOS&AppTime=1523250517&FlagChnl=1&AppId=iOS",
        # # 13 获取用户信息
        # "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiLLQueryEBankAcct&UserId=10719&Token=54a1f22a5800ba323bac7905bf307c6a&defidenshuxing=1&platformiOS=iOS&AppTime=1523250558&FlagChnl=1&AppId=iOS",
        # 14 充值页面 获取充值数据
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiLLQueryEBankAcct&UserId=10719&Token=a8866e02cae1a696673a361adc746a6e&defidenshuxing=1&platformiOS=iOS&AppTime=1523251579&FlagChnl=1&AppId=iOS",
        # 15 充值 -- 支付创单
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLNetSave&UserId=10719&Token=4aed492d25da2ad64510d9c85d33d822&defidenshuxing=1&TransAmt=1000.00&platformiOS=iOS&CmdId=LLNetSave&AppTime=1523251666&FlagChnl=1&AppId=iOS",
        # 16 我的首页—融托投资账户金额数据请求
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiGetUserInfo&Token=8339b8b53bc6cc2affd832b271831be6&UserId=11115&AppId=iOS&platformiOS=iOS&AppTime=1523245064&defidenshuxing=1",
        # 17 是否设置交易密码
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=QueryAcctPasswordIsSet&Token=42f36390327b8537162de0d64a39c95c&UserId=194&AppId=iOS&platformiOS=iOS&AppTime=1523245632&defidenshuxing=1&FlagChnl=1",
        # 18 交易密码设置-徽商web页面
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLPassWordSet&Token=42f36390327b8537162de0d64a39c95c&UserId=194&AppId=iOS&platformiOS=iOS&AppTime=1523245632&defidenshuxing=1&FlagChnl=1",
        # 19 提现列表
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiLLCashQuery&UserId=11115&Token=0685013cd73f9710bb7cc10c1e550031&defidenshuxing=1&platformiOS=iOS&AppTime=1523252179&FlagChnl=1&AppId=iOS",
        # # 20 取现提交-web页面
        # "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLCash&AppId=iOS&UserId=10877&AppTime=1523252546&Token=ada8e3adceb662553f48534ad74f2642&FlagChnl=1&TransAmt=123.00&TransType=1&BankCnaps=105471000030&BrabankName=中国建设银行股份有限公司聊城振兴路支行&defidenshuxing=2",
        # 21 提现开户行省份
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLGetProvince&UserId=194&Token=1d92f641df807f05af10a2cf809d9343&defidenshuxing=1&platformiOS=iOS&AppTime=1523252887&FlagChnl=1&AppId=iOS",
        # 22 提现开户行所在市
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLGetCity&UserId=194&defidenshuxing=1&Token=03f08ed2c11467e3f8f35f2b6596cd2e&Code=34&platformiOS=iOS&AppTime=1523252936&FlagChnl=1&AppId=iOS",
        # 23 提现开户行列表
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=Prcptcdquery&CardNo=6222081602005990337&UserId=194&defidenshuxing=1&Token=e3b2e9d092aaa115e1c1d08564202a43&platformiOS=iOS&CityCode=150500&AppTime=1523253017&FlagChnl=1&AppId=iOS",
        # 24 融托账户—我的债权（//项目状态jkzhuangtai（0：全部，6：未到期，8：已到期，10：冻结中））
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetMyZhaiQuan&UserId=12154&page_size=10&Token=48ee78f4cd49e230ebd10e69d6d2753d&defidenshuxing=1&platformiOS=iOS&txlx=0&jkzhuangtai=0&AppTime=1523253425&xmlx=0&page=1&AppId=iOS",
        # 25 账单-请求有月份数据的接口
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiGetDealMonthList&Token=47df4980cf8ed9602d933ba741f2e86f&UserId=12154&defidenshuxing=1&platformiOS=iOS&PageNum=1&AppTime=1523254322&DealTrench=0,1,2,3,4,5&AppId=iOS",
        # 26 账单-请求选中单独月份内的数据
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiGetDealDetailList&UserId=12154&Token=19ad4bd5944a6ba99d17ac28004ac1e8&defidenshuxing=1&platformiOS=iOS&TransMonth=2018-04&AppTime=1523254323&DealTrench=0,1,2,3,4,5&AppId=iOS",
        # 27 月账单
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiGetMonthDealStats&Token=fad38dfd71ef1eca604fd63563dd48e1&UserId=12154&defidenshuxing=1&platformiOS=iOS&AppTime=1523254748&SearchMonth=2017-12&AppId=iOS",
        # 28 交易密码设置-获取验证码
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=IdentifyCodeSend&AppId=iOS&UserId=11115&AppTime=1523255225&Token=e8f91db4be666e8d2d4a8458facc143b&FlagChnl=1&TransType=2&PhoneNum=13520227421&platformiOS=iOS&defidenshuxing=1",
        # # 29 交易密码设置-验证验证码
        # "https://www.rongtuojinrong.com/hsesb/esb?CmdId=IdentifyCodeCheck&AppId=iOS&UserId=11115&AppTime=1523255371&Token=715b83536a71aa461ac9050306318943&FlagChnl=1&TransType=2&PhoneNum=13520227421&Code=973816&platformiOS=iOS&defidenshuxing=1",
        # 30 项目信息页 数据
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetProjectInfo&Token=1c4aff423a149fb42c54d5cf22b070a0&UserId=9166&jie_id=3116&defidenshuxing=1&platformiOS=iOS&AppTime=1523254471&AppId=iOS",
        # 31 项目列表
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetAllProjectList&UserId=9166&pro_status=0&Token=c7a0d0516357288d37342abf9d037485&defidenshuxing=1&platformiOS=iOS&CmdId=GetAllProjectList&AppTime=1523254929&page=1&AppId=iOS&page_size=6",
        # 32 首页-悬浮米袋
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLPurseDisplay&Token=df987f0c7c37eb9dac3c79e59ac6b1a1&UserId=9166&AppId=iOS&platformiOS=iOS&AppTime=1523255010&defidenshuxing=1",
        # 33 用户开户成功后判断用户是否设置交易密码
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=QueryAcctPasswordIsSet&FlagChnl=1&UserId=9166&defidenshuxing=1&Token=f8d2fefcbe3127c6ad5b7714398f389c&AppTime=1523255004&AppId=iOS",
        # 34 确认投资-可用余额
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=mybalannumbendi&Token=22f6c196da8b58922c444ae76ad90db2&UserId=578&AppId=iOS&platformiOS=iOS&AppTime=1523257743&defidenshuxing=1",
        # 35 确认投资
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=LLBidApply&AppTime=1523258224&AppId=huiyuan&UserId=578&Token=b889db0da990b9f04d8df1c5500438b9&ProjId=1587&TransAmt=100.00&RedPacket=&InterestCoupon=",
        # 36 我的邀请（邀请过好友的）
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetInviterStats&Token=afb9ac2f34f9a7a2270802f2ae071d08&UserId=12154&AppId=iOS&platformiOS=iOS&AppTime=1523245389&defidenshuxing=1",
        # 37 奖励明细
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetInviterAwardList&AwardType=0&StartTime=1388505600&UserId=12154&Token=77f67545004d49852a15b4a210ae0e31&defidenshuxing=1&PageNum=1&platformiOS=iOS&AppTime=1523245556&EndTime=1523203200&AppId=iOS",
        # 38 我的卡券  -- 已使用和过期体验金
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetExperienceCoupon&Token=976ffd396a1e70215b13a642d9aebd2d&UserId=12154&Status=1,2&defidenshuxing=1&platformiOS=iOS&PageNum=1&AppTime=1523251394&AppId=iOS",
        # 39 绑定银行卡界面 ---- 解卡后绑卡接口
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BindCard&SigCard=1111111111111111111&platformiOS=iOS&UserId=126&AppTime=1523253022&Mobile=18953166668&FlagChnl=1&defidenshuxing=1&AppId=iOS&Token=02e9e11ae3fb9b890fde08ba3ed5323b",
        # 40 风险评估问卷
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetTest&Token=215f3496285fa4eeead4b87e87b7b23a&UserId=10719&defidenshuxing=1&platformiOS=iOS&TestCode=RiskAssessmentQuestionnaire&AppTime=1523250706&AppId=iOS",
        # 41 我的首页—获取用户评级（去评估）
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetUserGradeInfo&UserId=11115&Token=8339b8b53bc6cc2affd832b271831be6&defidenshuxing=1&platformiOS=iOS&CmdId=GetUserGradeInfo&AppTime=1523245064&AppId=iOS",
        #  42 融托投资账户单独金额数据请求
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=BendiGetUserInfodandu&Token=33b9334d8775b481f7e93b5c570b7198&UserId=194&AppId=iOS&platformiOS=iOS&AppTime=1523251036&defidenshuxing=1",
        # 43 项目信息页用于请求num字段判断加息行是否显示
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=GetInterestCouponNum&Token=f83c0ec6eebd175178108b7e54aad5ad&UserId=9166&ProjId=3116&defidenshuxing=1&platformiOS=iOS&AppTime=1523254436&AppId=iOS",
        # 44 项目-下拉列表
        "https://www.rongtuojinrong.com/hsesb/esb?CmdId=XingMuListCategory&UserId=9166&Token=f8d2fefcbe3127c6ad5b7714398f389c&defidenshuxing=1&platformiOS=iOS&CmdId=XingMuListCategory&AppTime=1523255004&AppId=iOS"
    ]

    now_time = round(time.time())

    url_error_arr = [] # 请求不相同的链接数组

    for i in range(len(url_array)):
        params = querys_params(url_array[i])
        params['AppTime'] = now_time
        user_id = params['UserId']
        token_str = "AppId=iOS&UserId=%s&AppTime=%d" % (user_id, now_time)
        hash = hashlib.md5()
        hash.update(token_str.encode('utf-8'))
        token_md5 = hash.hexdigest()
        params['Token'] = token_md5

        print("\n第%d个字典值:" % i, params)

        for j in range(0,10):
            result_www = get_www_data(www, params)
            result_php = get_php_data(php, params)

            if result_www[0] == result_php[0]:
                print("结果相同，接口正确")
            else:
                print("结果不同，接口错误")
                url_error_arr.append(url_array[i])

    print("出现错误的接口%d个：\n" % len(url_error_arr), url_error_arr)

if __name__ == '__main__':

    # time_bid = input("请输入测试时间，格式（14:00:00），点击enter：")
    user_id = input("请输入user_id，也可以不输入，点击enter：")
    # time_judge(time_bid,user_id)
    start_request_ten(user_id) # 每个请求 10 次
    # start_request_once() # 每个请求一次


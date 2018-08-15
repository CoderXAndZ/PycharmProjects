#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-

# 创建 excel 表格

# import xlwt
#
#
# wbk = xlwt.Workbook()
# sheet = wbk.add_sheet('sheet 1')
# # indexing is zero based, row then column
# sheet.write(0,1,'test text')
# sheet.write(1,1,'test text')
# wbk.save('/Users/admin/Desktop/接口测试结果统计/test2.xls')  # 默认保存在桌面上

import hashlib # md5 加密

token_str = "AppId=iOS&UserId=126&AppTime=1526020888"
hash = hashlib.md5()
hash.update(token_str.encode('utf-8'))
token_md5 = hash.hexdigest()

print("token_md5：%s"%token_md5)
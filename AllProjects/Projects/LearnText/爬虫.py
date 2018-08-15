#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-

# url:http://money.163.com/special/pinglun/
# 抓取网易新闻数据并格式化成json数据
# import urllib
# from urllib import request
# import re
#
# def get_content(url):
#     f = request.urlopen(url)
#     content = f.read().decode('gbk')
#     print(content)
#
#     regex = re.compile('<div class="item_top">\n                <h2><a href=".*?">.*?</a></h2>\n                                <a href="(.*?)" title="(.*?)" class="newsimg" lang=".*?"><img src="(.*?)" alt=".*?" /></a>                                <p>(.*?)<br />\n                    <span class="time">(.*?)</span>\n                </p>\n            </div>')
#     results = re.findall(regex,content)
#     print("结果是：",results)
#
#     f.close()
#
#     lists = []
#
#     for res in results:
#         lists.append({'title':res[1],'created_at':res[4],'url':res[0],'img':res[2],'content':res[3]})
#     return lists
#
# dic = get_content("http://money.163.com/special/pinglun/")
# print("格式化后的字典：",dic)

# import urllib
# from urllib import request
# from urllib import parse
# import re
# import logging
#
# def jd_search(keyword):
#     keyword_encode = parse.quote(keyword) # unquote 解码
#     url = "https://search.jd.com/Search?keyword=%s&enc=utf-8&wq=%s&pvid=ce136a5537cb437aa6217a24d35a1e02"%(keyword_encode,keyword_encode)
#     f = request.urlopen(url)
#     content = f.read().decode('utf-8') #.decode('utf-8')
#     print(content)
#
#     regex = re.compile('<div class="gl-i-wrap">.*?title="(.*?)" href="(.*?)".*?src="(.*?)".*?</div>',re.S)
#     results = re.findall(regex,content)
#
#     print("结果是：",results)
#
#     print("第一个值：",results[0])
#
#     f.close()
#
#     lists = []
#     for res in results:
#         lists.append({'title':res[0],'url':res[1],'img':res[2],})
#     return lists
#
# dict = jd_search("猫粮")
#
# print("json字典：",dict)


# url:https://search.jd.com/Search?keyword=%E5%B9%BC%E7%8C%AB%E7%8C%AB%E7%B2%AE&enc=utf-8&wq=%E5%B9%BC%E7%8C%AB%E7%8C%AB%E7%B2%AE&pvid=ce136a5537cb437aa6217a24d35a1e02
# import urllib
# from urllib import request
# from urllib import parse
# import re
# from bs4 import BeautifulSoup
#
# def jd_search(keyword):
#     keyword_encode = parse.quote(keyword) # unquote 解码
#     url = "https://search.jd.com/Search?keyword=%s&enc=utf-8&wq=%s&pvid=ce136a5537cb437aa6217a24d35a1e02"%(keyword_encode,keyword_encode)
#     f = request.urlopen(url)
#     content = f.read().decode('utf-8')
#     print(content)
#
#     soup = BeautifulSoup(content,'html.parser')
#
#     print("结果是：",soup.title)
#
#     results = soup.find_all('li')
#     print("第一个结果是：",results)
#
#     f.close()
#
# jd_search("猫粮")

# logger = logging.getLogger()
# hdlr = logging.FileHandler('/Users/admin/Desktop/修改IP/sendlog.txt')
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr)
# logger.setLevel(logging.NOTSET)
# logger.debug(results)


# URL:https://search.jd.com/s_new.php?keyword=鞋&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=xie&page=3&s=51&click=0
import urllib
import json
from urllib import parse,request
from bs4 import BeautifulSoup

# 根据页数和keywords采集内容
def get_content_from_keyword(keyword,page=1):
    # keyword_encode = parse.quote(keyword)  # unquote 解码
    # url = "https://search.jd.com/s_new.php?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%s&page=%d&s=51&click=0"%(keyword_encode,keyword_encode,page)
    # r = request.urlopen(url)
    params = {'keyword':keyword,'page':page,'enc':'utf-8','area':1,'wq':keyword}
    data = parse.urlencode(params)
    opener = request.urlopen("https://search.jd.com/Search?"+data)
    content = opener.read()
    opener.close()
    return content # .decode('utf-8')

# 模拟上滑加载的动作
def get_more_data(keyword):
    driver = webdriver.Firefox()
    driver.implicitly_wait(3)

    parse.quote(keyword)
    url = "https://search.jd.com/s_new.php?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%s&s=51&click=0"%(keyword_encode,keyword_encode)
    driver.get(url)
    print()
    return driver

# 分析数据，生成字典 res
if __name__ == '__main__':
    keyword = '裤子'
    content = get_content_from_keyword(keyword,3)
    soup = BeautifulSoup(content,"html.parser")
    goods_info = soup.select(".gl-item")

    res = []
    for good_info in goods_info:
        data = {}
        good_info_dict = good_info.select(".p-name.p-name-type-2 a")[0].attrs
        data['data_sku'] = good_info.attrs['data-sku']
        data['title'] = good_info_dict['title']
        data['href'] = good_info_dict['href']
        data['price'] = good_info.select('.p-price')[0].text.strip()
        res.append(data)
    print("\n\n\n商品信息：\n\n\n",goods_info,"\n\n\n格式化数据：",json.dumps(res,sort_keys=True, indent=2))

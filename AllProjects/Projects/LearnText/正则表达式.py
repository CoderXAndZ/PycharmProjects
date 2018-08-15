#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-


import re

# c = "1234353464"
# print(re.match('\d',c))
# print(re.match('\d','45'))
#
# print(re.match('\d+$','43'))
# print(re.match('\d?$','43'))

regx = re.match(r"^(\w+) (\w+)$",'hello world')

print(dir(regx))
print(regx.groups())

regx = re.match(r"^\w+ (\w+)$",'hello world')
print(regx.groups())

e = "a1b3c4n5m6"
res = re.split(r'\d',e)
print(res)


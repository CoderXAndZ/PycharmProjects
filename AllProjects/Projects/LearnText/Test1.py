#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
# FileName:Test1.py


# def add(*nums):
#     total = 0
#     for n in nums:
#         total += n
#     return  total
#
# print(add(1,2,3))
#
#
# def add(num1,num2):
#     if isinstance(num1,int) and isinstance(num2,int):
#         return num1 + num2
#     else:
#         return "参数里有不是数字的类型"
#
# print(add(3,4))
#
# assert add(2,3) == 5
# assert add(1,2) == 4


# treatises = ["Arithmetica","Conics","Elements"]
# str1 = " ".join(treatises)
# # str3 = "-<>-".join(treatises)
# str3 = "".join(reversed(treatises))
# # print(str3)
#
# s = "=" * 5
# s *= 3
# print(s)

"""
定义一个方法 get_num(num),num参数是列表类型，判断列表里面的元素为数字类型。
其他类型则报错，并且返回一个偶数列表。（注：列表里面的元素为偶数）。

def get_num(nums):
    if not isinstance(nums,list):
        return "输入的参数不是列表类型"
    else:
        numList = []
        for n in nums:
            if not isinstance(n,int):
                return "列表里面的元素不是数字类型"
            else:
                if n % 2 == 0:
                    numList.append(n)
        return numList

if __name__ == '__main__':
    ls = [1,2,3,4,5]
    print("输出结果:",get_num(ls))

    assert get_num([3,4,25,6]) == [3,4,25,6]
    assert get_num([1,3,'aa','qwer']) == "列表里面的元素是数字类型"
    assert get_num((1,2,3,4,5,10)) == "输入的参数不是列表类型"

"""

# def fun1(arg1,arg2):
#     return arg1 + arg2
#
# print(dir(fun1.__code__))
# """
# ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'co_argcount', 'co_cellvars', 'co_code', 'co_consts', 'co_filename', 'co_firstlineno', 'co_flags', 'co_freevars', 'co_kwonlyargcount', 'co_lnotab', 'co_name', 'co_names', 'co_nlocals', 'co_stacksize', 'co_varnames']
# """
# print(fun1.__code__.co_varnames)
# """
# ('arg1', 'arg2')
# """
# print(fun1.__code__.co_filename)
# """
# /Users/admin/PycharmProjects/untitled1/venv/LearnText/Test1.py
# """
# print(help(fun1.__code__))


# global arg
#
# arg = 1
#
# def fun1():
#     global arg
#     arg = 3
#
# fun1()
#
# print(arg)

# def fun1(arg):
#     if not isinstance(arg,list):
#         return "输入的不是列表类型"
#     # 修改列表的第一个参数值
#     arg[0] = 5
#     return arg
#
# tlist = [1,2,3,4,6]
# print(tlist,"\n",fun1(tlist))
# """
# 输出结果：列表本身被修改
# [5, 2, 3, 4, 6]
# [5, 2, 3, 4, 6]
# """

d = lambda x:x+1 if x>0 else "error"

def add(x):
    return x+1

"""
lambda 与函数

相同点：
    1>lambda 函数与add函数实现的功能一样；
    2>lambda 也是可以直接使用三元运算符的,例如：
        d = lambda x:x+1 if x>0 else "error"
        print(d(-2))  # 输出结果：error
    3>也可以使用列表推导
        g = lambda x:[(x,i) for i in  range(0,10)]

        print(g(10)) #输出结果：[(10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9)]
 
区别：
    1>lambda 没有return，其实是隐藏了一个return；而函数如果没有return，我们就无法得到函数的结果;
    2>lambda 不可以在里面使用一些常规的if语句或者for语句、while语句等;
# """

# # 查看是否可以使用列表推导：
# g = lambda x:[(x,i) for i in  range(0,10)]
#
# print(g(10)) #输出结果：[(10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9)]
#
# print(d(-2))

# t = [1,2,3,4,5]
# fun = filter(lambda x:x > 3,t)
#
# print(list(fun))

# def func(arg1,arg2,arg3):
#     return arg1,arg2,arg3
#
# print(func(1,2,3)) # (1, 2, 3)

# def func(k1='',k2=None,k3=''):
#     return k1,k2,k3
#
# print(func(k3=1,k1=5)) # (5, None, 1)
# print(func(k1=5,k3=1)) # (5, None, 1)
# print(func(k3=1,k1=5,k2=3)) # (5, 3, 1)

"""
定义一个函数 def detail(name=None,**kwargs)，实现效果如下：

assert detail("lilei") == "lilei"
assert detail("lilei",years=4) == "lilei,years:4"
assert detail("lilei",years=4,heigtht=1.81) == "lilei,years:4,heigtht:1.81"
"""
def detail(name=None,**kwargs):
    lis = ["%s:%s"%(k,v) for k,v in kwargs.items()]
    lis.insert(0,name)
    return ','.join(lis)

assert detail("lilei") == "lilei"
assert detail("lilei",years=4) == "lilei,years:4"
assert detail("lilei",years=4,heigtht=1.81) == "lilei,years:4,heigtht:1.81"

a = [1,3,4,5,6,7]
b = filter(lambda x: x > 5,a)
print(list(b))
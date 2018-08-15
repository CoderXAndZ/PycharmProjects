# import threading
# import random
#
# def test():
#     num = random.uniform(1,10)
#     print('第',num,'个线程')
#
# a = threading.Thread(target=test())
# b = threading.Thread(target=test())
# a.start()
# b.start()
#
# a.join() # join等待其他线程退出以后，再执行join后面的代码
# b.join()


# # 多个线程
# import threading
# import time
#
# def test(p):
#     time.sleep(0.001)
#     print(p)
#
# ts = []
#
# for i in range(0,15):
#     th = threading.Thread(target=test,args=[i])
#     ts.append(th)
#
# for i in ts:
#     i.start()
#
# for i in ts:
#     i.join()
#
# print("回到主线程")

# import threading
#
# num = 0
#
# def t():
#     global num
#     num += 1
#     print(num)
#
# for i in range(0,10):
#     d = threading.Thread(target=t)
#     d.start()

# import time
#
# def a():
#     print('a start')
#     time.sleep(2)
#     print('a end')
#
# def b():
#     print('b start')
#     time.sleep(3)
#     print('b end')

# b_time = time.time()
# a()
# b()
# print(time.time() - b_time)

""" 输出结果：
a start
a end
b start
b end
5.005458831787109
"""
#
# import threading
#
# begin_time = time.time()
#
# _a = threading.Thread(target=a) # 注意：target后面只能跟方法名a,不能跟a(),这样相当于没开线程
# _b = threading.Thread(target=b)
#
# _a.start()
# _b.start()
#
# _a.join()
# _b.join()
#
# print(time.time() - begin_time)

"""输出结果：
a start
b start
a end
b end
3.0049290657043457
"""


# # 加锁和释放锁的简单实例
# import threading
#
# mlock = threading.Lock()
#
# num = 0
#
# def test():
#     global num
#     mlock.acquire() # 加锁
#     num += 1 # 需要执行的代码
#     mlock.release() # 释放锁
#     print(num)
#
# for i in range(0,5):
#     d = threading.Thread(target=test)
#     d.start()


# # 协程
# a = [1,2,3,4]
#
# for i in a:
#     print(i,'\n\n\n')
#
# # yield 实现
# def test():
#     i = 0
#     a = 4
#     while i < a:
#         x = yield i # 每一次碰到 yield 的时候就会把这个值返回给我们
#         i += 1
# # for i in test():
# #     print(i)
#
# t = test()
# print(t)
# print(t.__next__())


# def test():
#     x = yield '第一步，会直接返回'
#     print('第一步 %s'%x)
#     x = yield '%s 每次请求，不管是send，还是next,都会往下一直跑到下一个yield，并且把yield后面的值返回回来'%x
#     print('第二步 %s'%x)
#     x = yield
#
# t = test()
# print(t.__next__())
# print('\n',t.send('给第一个x赋值'))
# print('\n\n',t.send('给第二个x赋值'))
# print('\n\n\n',t.__next__())


# print(t.send('给第二个x赋值'))

"""
输出结果：
第一步，会直接返回
第一步 给第一个x赋值

 给第一个x赋值 每次请求，不管是send，还是next,都会往下一直跑到下一个yield，并且把yield后面的值返回回来
第二步 给第二个x赋值


 None
"""

# 有10个刷卡机，代表建立10个线程，每个刷卡机每天扣除用户一块钱进入总账中，
# 每个刷卡机每天账户原有500块。所以，当天最后的总账应该为1500。

# import threading
# import time
#
# mlock = threading.Lock()
#
# num = 500
#
# def deduct_money():
#     global num
#
#     for i in range(0,100): # 每个刷卡机每天一共被刷100次
#         mlock.acquire()
#         num += 1
#         mlock.release()
#
# begin_time = time.time()
#
# lists = []
# for i in range(0,10):
#     d = threading.Thread(target=deduct_money)
#     d.start()
#     lists.append(d)
#
# for i in lists:
#     i.join()
#
# print("当天最后总账为：",num) # 当天最后的总账应该为1500
# print("耗时",time.time() - begin_time)


# def febir(num):
#     x,y = 1,1
#     while x < num:
#         yield x
#         x,y = y,x + y
#
# for i in febir(9999):
#     print(i)

def sushu(num):
    if num == 1:
        return False
    elif num == 2:
        return False
    else:
        for i in range(2, num):
            if num % i == 0:
                return False
        return True

a = [i for i in range(1,101) if sushu(i)]

print("素数",a)
#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 返回请求结果的多线程

from threading import Thread

class ThreadGetResult(Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):

        Thread.__init__(self,group,target,name,args,kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def get_result(self):
        try:
            return self.result # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

    # def join(self):
    #     Thread.join(self)
    #     return self._return




    # def __init__(self,func,args=()):
    #     super(ThreadGetResult, self).__init__()
    #     self.func = func
    #     self.args = args
    #
    # def run(self):
    #     self.result = self.func(*self.args)
    #
    # def get_result(self):
    #     try:
    #         return self.result # 如果子线程不使用join方法，此处可能会报没有self.result的错误
    #     except Exception:
    #         return None

    # 调用
    # # thread_www.join()
    # # result_www = thread_www.get_result()
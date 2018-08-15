
import time

global total

# 类似倒计时功能实现
def start(total_time):
    while (total_time > 0):
        print("total_time:", total_time)
        time.sleep(1)
        total_time -= 1

def end():
    print("调用停止打印")
    start(0)

if __name__ == '__main__':
    global total
    total = 10
    start(total)
    end()
    print("结束了")

    # # 类似倒计时功能实现
    # count = 0
    # total = 5
    # while (total > count):
    #     print("total:", total)
    #     time.sleep(1)
    #     total -= 1
    #
    # print("结束了")
#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# FileName:ChangeIP.py

import sys
import os, tempfile, webbrowser, random
import wmi, time
from twisted.web import client
from twisted.internet import reactor

print ("正在修改IP,请稍后...")

# 修改IP地址
def ModifyIP(ip,mask,gateway):
    wmiService = wmi.WMI()
    colNicConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled = True)

    if len(colNicConfigs) < 1:
        print("没有找到可用的网络适配器")
        exit()

    # 选择要修改的网卡
    objNicConfig = colNicConfigs[0]

    print("目前配置为：IP：%s",objNicConfig.IPAddress + "掩码：%s",objNicConfig.IPSubnet + "网关：%s",objNicConfig.DefaultIPGateway)

    arrIPAddresses = [ip]
    arrSubnetMasks = [mask]
    arrDefaultGateways = [gateway]
    arrGatewayCostMetrics = [1]

    intReboot = 0

    returnValue = objNicConfig.EnableStatic(IPAddress=arrIPAddresses,SubnetMask=arrSubnetMasks)

    print("returnValue的值：",returnValue)

    if returnValue[0] == 0:
        print("设置IP成功")
    elif returnValue[0] == 1:
        print("设置IP成功")
        intReboot += 1
    else:
        print("修改IP失败：IP设置发生错误")
        sys.exit()

    returnValue = objNicConfig.SetGateways(DefaultIPGateway=arrDefaultGateways,GatewayCostMetric=arrGatewayCostMetrics)

    if returnValue[0] == 0:
        print("设置网关成功")
    elif returnValue[0] == 1:
        print("设置网关成功")
        intReboot += 1
    else:
        print("设置网关失败：网关设置发生错误")
        exit()

    if intReboot > 0:
        print("需要重新启动计算机")
    else:
        print("修改后的配置为：IP：%s",objNicConfig.IPAddress + "掩码：%s",objNicConfig.IPSubnet + "网关：%s",objNicConfig.DefaultIPGateway)

# 主函数
def main():
    sysargv = sys.argv
    prefix = sys.argv[1]
    start = sys.argv[2]
    end = sys.argv[3]
    mask = sys.argv[4]
    gateway = sys.argv[5]

    ipList = []
    for i in range(int(start),int(end)+1):
        ipList.append(prefix + str(i))

    for ip in ipList:
        ModifyIP(ip,mask,gateway)
        time.sleep(3)

if __name__ == '__main__':
    main()
#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 寻找Xcode中不使用的文件


import glob
import os
import re

# path = '/Users/admin/iosdeleteYoushangcheng/fmapp/classes'

all_files = [] # 所有的.m文件

# 递归查询到所有的 .m 文件并加入到 all_files 数组
def find_all_ponintM_files(filePath_array):
    print("长度：", len(filePath_array),"当前文件路径数组是：",filePath_array)

    for file in filePath_array:
        files_inner = glob.glob(r'%s/*' % file)

        if len(files_inner) == 0:
            print("\n最终获得路径",file)
            # print("\n最终获得路径倒数2位",file[len(file)-2:len(file)])
            if ".m" in file[len(file)-2:len(file)] and ('AppDelegate' not in file) and ('+' not  in file): # 最后2位 是 .m 文件
                # array_str = file.split('/') # 以 / 分隔字符串
                # print("分隔的数组是：",array_str)
                # last_str = array_str[len(array_str) - 1][:-2]
                last_str = os.path.basename(file)[:-2] # 获取最后一个 *.m 中的 *
                print("最后一个字符串是：",last_str)
                all_files.append(last_str)
                print("添加到数组:",last_str)
        else:
            find_all_ponintM_files(files_inner)

unused_files = []
# 查找未使用的 .m 文件
def find_un_used(array):
    file_names = [os.path.basename(file) for file in array]

    for i in range(0, len(array)):
        file_name = file_names[i]
        print("文件名字", file_name)
        command = 'ag "%s" %s' % (file_name, path)
        print("command是 ==== ",command)
        result = os.popen(command).read()
        print("\n执行结果：", result, "\n")

        string = '[%s' % file_name # 创建代码，例如： [[WLJYJViewController alloc] init];
        extensionClass = '(%s)' % file_name  # 分类
        # print("分类数据",extensionClass)
        thirdTool = 'https://github.com/*/%s' % file_name # 第三方 好像不对
        print("是否是第三方：",re.match(thirdTool, file_name))

        XMPPThirdTool = file_name[0:4]  # 是XMPP第三方工具类都不添加

        if result == '':
            unused_files.append(file_name)
        elif (string in result) or (extensionClass in result) or re.match(thirdTool, file_name): #  and ('YYGestureRecognizer' == file_name) and ('YYC' not in file_name[0:3]) and ('YYText' not in file_name[0:6]) and ('YYThread' not in file_name[0:8])
            print("有引用")
        elif ('XMPP' not in XMPPThirdTool) and ('AFURL' not in file_name[0:5]) and ('XEP_0223' not in file_name) and ('WPTappableLabel' not in file_name) and ('Data' not in file_name[0:4]) and ('MD5DataSigner' not in file_name) and ('openssl_wrapper' not in file_name) and ('YY' not in file_name[0:2]) and ('DD' not in file_name[0:2]) and ('JH' not in file_name[0:2])  and ('MJ' not  in file_name[0:2]) and ('SD' not  in file_name[0:2]) and ('H' not in file_name[0:1]) and ('I' not in file_name[0:1]):
            unused_files.append(file_name)
            # print("\n可能没有引用的文件是：", unused_files)

if __name__ == '__main__':

    path = input("输入项目所有的.h和.m文件的所在的上层文件夹，例如Class文件夹：\n")

    files = glob.glob(r'%s/*' % path)  # 找到filePath中所有的下级文件或文件夹

    find_all_ponintM_files(files)

    print("\n长度",len(all_files),"所有的.m文件：", all_files)

    # 查找未使用的 .m 文件
    find_un_used(all_files)
    print("\n个数", len(unused_files), "\n可能没有引用的文件是：", unused_files)

    # 将确定使用的类存放在数组中进行过滤
    array = ['AddbabyPlanTableViewCell','BabyPlayDetailTableViewCell','FMFunctions','FMGoodShopHeaderModel','FMIMBaseTableVIewCell','FMIMInputContentView','FMShopSpecModel','FMTradeNoteNewController','FMTradeNoteTableViewCell','FMViewController','FSCalendarConstants','LLLockViewController','LRLAVPlayerTool','LRLLightView','LTSCalendarContentView','LTSCalendarManager','LTSCalendarSelectedWeekView','LTSCalendarWeekDayView','LWImageBrowserButton','LWLayout','NSDataEx','RFImageToDataTransformer','TADotView','TURNSocket','TimeSheetView','XMConverNoteCell','XZGetTogetherNewCell']

    final_file = []
    for unused_file in unused_files:
        if unused_file not in array: # 判断某个元素是否在数组中
            final_file.append(unused_file)

    text_path = 'unusedFile.txt'
    tex = '\n'.join(sorted(final_file))
    os.system('echo "%s" > %s' % (tex, text_path))


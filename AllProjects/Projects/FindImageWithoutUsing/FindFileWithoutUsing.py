#! /usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 寻找Xcode中不使用的文件


import glob
import os
import re

path = '/Users/admin/iosdeleteYoushangcheng/fmapp/classes'

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
                array_str = file.split('/') # 以 / 分隔字符串
                print("分隔的数组是：",array_str)
                last_str = array_str[len(array_str) - 1][:-2] # 获取最后一个 *.m 中的 *
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
        if (string in result) or (extensionClass in result) or re.match(thirdTool, file_name):
            print("有引用")
        else:
            unused_files.append(file_name)
            # print("\n可能没有引用的文件是：", unused_files)

if __name__ == '__main__':

    files = glob.glob(r'%s/*' % path)  # 找到filePath中所有的下级文件或文件夹

    find_all_ponintM_files(files)

    print("\n长度",len(all_files),"所有的.m文件：", all_files)

    unused_files_path = 'unusedFileName.txt'
    text_content = '\n'.join(sorted(all_files))
    os.system('echo "%s" > %s' % (text_content, unused_files_path))

    # array = []
    # for i in range(0,9):
    #     array.append(all_files[i])
    #     find_un_used(array)

    # 查找未使用的 .m 文件
    find_un_used(all_files)

    print("\n个数",len(unused_files),"\n可能没有引用的文件是：", unused_files)
    text_path = 'unusedFile.txt'
    tex = '\n'.join(sorted(unused_files))
    os.system('echo "%s" > %s' % (tex, text_path))
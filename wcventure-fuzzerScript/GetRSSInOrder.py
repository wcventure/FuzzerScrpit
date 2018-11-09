#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import getopt
import os
import time
import datetime

def main(argv):
    #通过 getopt模块 来识别参数demo

    TargetFolder = ""
    CommandLine = ""

    try:

        opts, args = getopt.getopt(argv, "hc:f:", ["help", "CommandLine=", "TargetFolder="])


    except getopt.GetoptError:
        print('Error: GetRSSInOrder.py -f <TargetFolder>')
        sys.exit(2)

    # 处理 返回值options是以元组为元素的列表。
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('GetRSSInOrder.py -c <CommandLine> -f <TargetFolder>')
            sys.exit()
        elif opt in ("-c", "--command"):
            CommandLine = arg
        elif opt in ("-f", "--folder"):
            TargetFolder = arg
        
    if TargetFolder == "":
        print('Error: TargetFolder is empty')
        print('Tips: Using -h to view help')
        sys.exit(2)
    if CommandLine == "":
        print('Error: Command Line is empty')
        print('Tips: Using -h to view help')
        sys.exit(2)
    
    if not TargetFolder[-1] == '/':
        TargetFolder = TargetFolder + '/'
        
    print('Command line = ', CommandLine)
    print('Target folder = ', TargetFolder)
    print('')        


    # 打印 返回值args列表，即其中的元素是那些不含'-'或'--'的参数。
    for i in range(0, len(args)):
        print('参数 %s 为：%s' % (i + 1, args[i]))


    # start
    fileList = []
    RSSLIST = []
    
    for i in os.walk(TargetFolder):
        for eachfile in i[2]:
            if eachfile[-2: ] == 'py':
                continue   #过滤掉.py文件
            fileList.append(eachfile)

    fileList.sort()

    # 依次文件
    for eachfile in fileList:
        with open (TargetFolder + eachfile, 'r') as f:
            TOP_MEM_List = []
            for line in f.readlines():
                if 'TOP_MEM_' in line:
                    left,right = line.split(':',1)
                    a,b,c = right.split(',',2)
                    TOP_MEM_List.append(a.strip())

            for each in TOP_MEM_List:
                print(each)
            print('')

        RSS_tmp_list = []
        if TOP_MEM_List != []:
            if os.path.exists('2.txt'):
                    os.system('rm -rf 2.txt')
            for eachTop in TOP_MEM_List:
                os.system('(/usr/bin/time --f %M '+ CommandLine + ' ' + eachTop + ') 2>> 2.txt')
            with open ('2.txt', 'r') as two:
                for line in two.readlines():
                    RSS_tmp_list.append(int(line))

            if os.path.exists('2.txt'):
                    os.system('rm -rf 2.txt')
            RSS_tmp_list.sort()

            # average
            RSSTOTAL = 0
            for i in range(1, len(RSS_tmp_list)-1):
                RSSTOTAL += RSS_tmp_list[i]
            RSSLIST.append(int(RSSTOTAL/(len(RSS_tmp_list)-2)))
        print(RSSLIST)

    # out
    with open ('./rss.txt', 'w+') as fi:
        if not RSSLIST == []:
            fi.write('RSS:\n')
            for each in RSSLIST:
                fi.write(str(each)+'\t')
            fi.write('\n')

    # end

	
if __name__ == "__main__":
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以用sys.argv[1:]过滤掉脚本名。
    starttime = datetime.datetime.now()

    main(sys.argv[1:])
    
    endtime = datetime.datetime.now()
    
    print ("start time: ", starttime)
    print ("end time: ", endtime)
    print ("The output can be seen in tmp.txt")
    print ("@@@ Finished @@@")

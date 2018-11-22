#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import getopt
import os
import time
import datetime

# -d 取900为15分钟

def main(argv):
    #通过 getopt模块 来识别参数demo

    TargetFile = ""
    OutputPath = ""
    DelayTime = ""

    try:

        opts, args = getopt.getopt(argv, "ht:o:d:", ["help", "TargetFile=","OutputPath=","DelayTime="])



    except getopt.GetoptError:
        print('Error: CaptureFuzzerStats.py -t <TargetFile> -o <OutputPath> -d <DelayTime>')
        print('   or: CaptureFuzzerStats.py --target=<TargetFile> --output=<OutputPath> --delay <DelayTime>')
        sys.exit(2)

    # 处理 返回值options是以元组为元素的列表。
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('CaptureFuzzerStats.py -t <TargetFile> -o <OutputPath> -d <DelayTime>')
            print('or: CaptureFuzzerStats.py --target=<TargetFile> --output=<OutputPath> --delay <DelayTime>')
            sys.exit()
        elif opt in ("-t", "--target"):
            TargetFile = arg
        elif opt in ("-o", "--output"):
            OutputPath = arg
        elif opt in ("-d", "--delay"):
            DelayTime = arg

    if TargetFile == "":
        print('Error: Command line is empty')
        print('Tips: Using -h to view help')
        sys.exit(2)
    if OutputPath == "":
        print('Error: Crash folder is empty')
        print('Tips: Using -h to view help')
        sys.exit(2)
    if DelayTime == "":
        print('Error: Crash folder is empty')
        print('Tips: Using -h to view help')
        sys.exit(2)

    if not OutputPath[-1] == '/':
        OutputPath = OutputPath + '/'
    
    print('Target file = ', TargetFile)
    print('Output Path =', OutputPath)
    print('Delay Time =', DelayTime)
    print('')        


    # 打印 返回值args列表，即其中的元素是那些不含'-'或'--'的参数。
    for i in range(0, len(args)):
        print('参数 %s 为：%s' % (i + 1, args[i]))


    # start
    
    for k in range(1, 99):
        time.sleep(int(DelayTime))
        if k==0 or k==1 or k==2 or k ==3 or k==4 or k==5 or k==6 or k==7 or k==8 or k==9:
            name = '0' + str(k)
        else:
            name = str(k)
        os.system("cp " + TargetFile + " " + OutputPath + name + ".txt")
        print("cp " + TargetFile + " " + OutputPath + name + ".txt")

    print("\nFinished: ALL")

    # end

	
if __name__ == "__main__":
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以用sys.argv[1:]过滤掉脚本名。
    starttime = datetime.datetime.now()

    # print ("\nstart time: ", starttime)

    main(sys.argv[1:])
    
    endtime = datetime.datetime.now()
    
    # print ("start time: ", starttime)
    # print ("end time: ", endtime)

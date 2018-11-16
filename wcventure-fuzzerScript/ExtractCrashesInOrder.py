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

    try:

        opts, args = getopt.getopt(argv, "hf:", ["help", "TargetFolder="])


    except getopt.GetoptError:
        print('Error: ExtractCrashesInOrder.py -f <TargetFolder>')
        sys.exit(2)

    # 处理 返回值options是以元组为元素的列表。
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('ExtractCrashesInOrder.py -f <TargetFolder>')
            sys.exit()
        elif opt in ("-f", "--folder"):
            TargetFolder = arg
        
    if TargetFolder == "":
        print('Error: Command line is empty')
        print('Tips: Using -h to view help')
        sys.exit(2)
    
    if not TargetFolder[-1] == '/':
        TargetFolder = TargetFolder + '/'
    
    print('Target folder = ', TargetFolder)
    print('')        


    # 打印 返回值args列表，即其中的元素是那些不含'-'或'--'的参数。
    for i in range(0, len(args)):
        print('参数 %s 为：%s' % (i + 1, args[i]))


    # start
    fileList = []
    UniqueCrashList = []
    TotalCrashList = []
    UniqueLeakList = []
    UniqueHangList = []
    
    SLenList = []
    MSizeList = []

    for i in os.walk(TargetFolder):
        for eachfile in i[2]:
            if eachfile[-2: ] == 'py':
                continue   #过滤掉.py文件
            fileList.append(eachfile)

    fileList.sort()

    # 依次文件
    for eachfile in fileList:
        with open (TargetFolder + eachfile, 'r') as f:
            TopNum = 0
            SLenTotal = 0
            MSizeTotal = 0
            for line in f.readlines():
                if 'unique_crashes' in line:
                    left,right = line.split(':',1)
                    UniqueCrashList.append(right.strip())
                if 'total_crashes' in line:
                    left,right = line.split(':',1)
                    TotalCrashList.append(right.strip())
                if 'unique_hangs' in line:
                    left,right = line.split(':',1)
                    UniqueHangList.append(right.strip())
                if 'unique_leaks' in line:
                    left,right = line.split(':',1)
                    UniqueLeakList.append(right.strip())
                
                if 'TOP_MEM_' in line:
                    TopNum += 1
                    left,right = line.split(':',1)
                    a,b,c = right.split(',',2)
                    SLenTotal += int(b.strip())
                    MSizeTotal += int(c.strip())
            if TopNum == 0:
                SLenList.append(0)
                MSizeList.append(0)
            else:
                SLenList.append(int(SLenTotal/TopNum))
                MSizeList.append(int(MSizeTotal/TopNum))


    with open ('./tmp.txt', 'w+') as fi:
        if not UniqueCrashList == []:
            fi.write('unque_crashes:\n')
            for each in UniqueCrashList:
                fi.write(each+'\t')
            fi.write('\n')
                
        if not TotalCrashList == []:
            fi.write('total_crashes:\n')
            for each in TotalCrashList:
                fi.write(each+'\t')
            fi.write('\n')

        if not UniqueHangList == []:
            fi.write('unique_hangs:\n')
            for each in UniqueHangList:
                fi.write(each+'\t')
            fi.write('\n')

        if not UniqueLeakList == []:
            fi.write('unique_leaks:\n')
            for each in UniqueLeakList:
                fi.write(each+'\t')
            fi.write('\n')
        if not SLenList == []:
            fi.write('SLen:\n')
            for each in SLenList:
                fi.write(str(each)+'\t')
            fi.write('\n')
        if not MSizeList == []:
            fi.write('MSize:\n')
            for each in MSizeList:
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

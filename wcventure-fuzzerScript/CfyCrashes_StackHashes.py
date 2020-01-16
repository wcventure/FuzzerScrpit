#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import getopt
import os
import time
import datetime
import csv
import re

def main(argv):
    #通过 getopt模块 来识别参数demo

    LogFile = ""

    try:

        opts, args = getopt.getopt(argv, "hi:", ["help", "LogFile="])

    except getopt.GetoptError:
        print('Error: CfyCrashes.py -i <LogFile>')
        sys.exit(2)

    # 处理 返回值options是以元组为元素的列表。
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('CfyCrashes.py -i <LogFile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            LogFile = arg
        
    if LogFile == "":
        print('Error: LogFile path is empty')
        print('Tips: Using -h to view help')
        sys.exit(2)
       
    print('Target folder = ', LogFile)
    print('')        


    # 打印 返回值args列表，即其中的元素是那些不含'-'或'--'的参数。
    for i in range(0, len(args)):
        print('参数 %s 为：%s' % (i + 1, args[i]))


    # start
    
    InputNameList = []
    crashTypeList = []
    crashDescriptionList = []
    LeakByte = 0
    LeakAllocation = 0

    
    Name = ''
    CrashType = ''
    CrashDesc = ''
    with open (LogFile, 'rb') as f:
        bugID = 0
        for temp_line in f.readlines():
            line = ""
            try:
                line = temp_line.decode("utf-8")
            except:
                pass
            if "--- go on ---" in line:
                Name = ''
                CrashType = ''
                CrashDesc = ''
            elif "File Name:" in line:
                rindex = line.rfind('/')
                Name = line[rindex+1:].strip()
            elif "ERROR: AddressSanitizer: requested allocation size" in line or "WARNING: AddressSanitizer: requested allocation size" in line:
                CrashType = 'Failed-to-allocate'
            elif "ERROR: AddressSanitizer:" in line:
                rindex = line.rfind(':')
                tmp = line[rindex+1:].strip()
                left, right = tmp.split(' ',1)
                CrashType = left.strip()
            elif "WARNING: AddressSanitizer" in line or "ERROR: AddressSanitizer" in line:
                rindex = line.find(':')
                
                if "failed to allocate" in  line and 'WARNING' in line:
                    CrashType = 'Failed-to-allocate'
                elif "failed to allocate" in  line and 'ERROR' in line:
                    CrashType = 'Failed-to-allocate'
                else:
                    tmp = line[rindex+1:].strip()
                    left, right = tmp.split(' ',1)
                    CrashType = left.strip()                
            elif "SUMMARY: AddressSanitizer"  in line:
                CrashDesc = line.strip()
                if "leaked" in line and "allocation" in line:
                    CrashType = "memory leaks"
                    tupleLA = re.findall(r"\d+", line)
                    LeakByte = LeakByte + int(tupleLA[0])
                    LeakAllocation = LeakAllocation + int(tupleLA[1])
            elif "AddressSanitizer CHECK failed" in line:
                index = line.find('AddressSanitizer CHECK failed')
                tmp = line[index:].strip()
                CrashDesc = tmp.strip()
            elif "#" in line:
                tmplist = re.findall(r"\d+:\d+",line)
                if not tmplist == []:
                    ll ,rr = tmplist[0].split(':',1)
                    bugID = bugID + int(ll)
            if "Aborted (core dumped)" in line or "Aborted" in line or "SUMMARY: AddressSanitizer: " in line:
            #if "SUMMARY: AddressSanitizer: " in line:
                InputNameList.append(Name)
                crashTypeList.append(CrashType + '-' + str(bugID))
                crashDescriptionList.append(CrashDesc)
                # print(Name, CrashType, CrashDesc)
                bugID = 0
                print(Name)

    # Statistics

    UniqueCrashList = set(crashDescriptionList)
    UniqueCrashNum = len(UniqueCrashList)
    print('TotalCrashNum = ', UniqueCrashNum)
    print('UniqueCrashNum = ', len(InputNameList))
    print('----------------------------')

    TypeSet = set(crashTypeList)
    UniqueTypeList = list(TypeSet)
    UniqueNumList = []
    for i in range(0, len(UniqueTypeList)):
        UniqueNumList.append(0)
        
    for i in range(0, len(UniqueTypeList)):
        for each in crashTypeList:
            if each == UniqueTypeList[i]:
                UniqueNumList[i] += 1

    for i in range(0, len(UniqueTypeList)):
        print(str(UniqueTypeList[i]),',',str(UniqueNumList[i]))
    print('----------------------------')
    for each in UniqueCrashList:
        print(each.replace('SUMMARY: ',''))
    print('')

    
            
    # out
    with open('./cfyList.csv' , 'w+') as fi:
        csv_write = csv.writer(fi, dialect='excel')
        csv_write.writerow(['InputName','CrashType','Description'])
        if not InputNameList == []:
            for i in range(0, len(InputNameList)):
                csv_write.writerow([InputNameList[i],crashTypeList[i],crashDescriptionList[i]])
            csv_write.writerow([])
            csv_write.writerow([])
            csv_write.writerow(['TotalCrashNum', UniqueCrashNum])
            csv_write.writerow(['UniqueCrashNum', len(InputNameList)])
            csv_write.writerow([])
            csv_write.writerow([])
            for i in range(0, len(UniqueTypeList)):
                csv_write.writerow([str(UniqueTypeList[i]),str(UniqueNumList[i])])
            csv_write.writerow([])
            csv_write.writerow([])
            csv_write.writerow(["Leak Byte(s)", LeakByte, "byte(s)"])
            csv_write.writerow(["Leak Allocation(s)", LeakAllocation, "allocation(s)"])
            
        print('@@@ write over @@@\n')
    
    '''
    with open ('./cfyList.txt', 'w+') as fi:
        if not InputNameList == []:
            fi.write('InputName\tCrashType\tDescription\n')
            for i in range(0,len(InputNameList)-1):
                fi.write(InputNameList[i]+'\t'+crashTypeList[i]+'\t'+crashDescriptionList[i]+'\n')
            fi.write('\n')
    '''     
    # end

	
if __name__ == "__main__":
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以用sys.argv[1:]过滤掉脚本名。
    starttime = datetime.datetime.now()

    main(sys.argv[1:])
    
    endtime = datetime.datetime.now()
    
    print ("start time: ", starttime)
    print ("end time: ", endtime)
    print ("The output can be seen in cfyList.csv")
    print ("@@@ Finished @@@")

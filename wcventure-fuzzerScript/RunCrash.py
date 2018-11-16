#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import getopt
import os
import time
import datetime

def main(argv):
    #通过 getopt模块 来识别参数demo

    Command = ""
    CrashPath = ""
    OutputFile = ""

    try:

        opts, args = getopt.getopt(argv, "hc:i:o:", ["help", "CommandLine=","CrashPath=","OutputFile="])

    except getopt.GetoptError:
        print('Error: RunCrash.py -c <CommandLine> -i <CrashFolder> -o <OutputFile>')
        print('   or: RunCrash.py --comand=<CommandLine> --crashfolder=<CrashFolder> --output OutputFile')
        sys.exit(2)

    # 处理 返回值options是以元组为元素的列表。
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('RunCrash.py -c <CommandLine> -i <CrashFolder> -o <OutputFile>')
            print('or: RunCrash.py --Command=<CommandLine> --crashfolder=<CrashFolder> --output <OutputFile>')
            sys.exit()
        elif opt in ("-c", "--Command"):
            Command = arg
        elif opt in ("-i", "--crashfolder"):
            CrashPath = arg
        elif opt in ("-o", "--output"):
            OutputFile = arg

    if Command == "":
        print('Error: Command line is empty')
        print('Tips: Using -h to view help')
        sys.exit(2)
    if CrashPath == "":
        print('Error: Crash folder is empty')
        print('Tips: Using -h to view help')
        sys.exit(2)
    if OutputFile == "":
        print('Error: Crash folder is empty')
        print('Tips: Using -h to view help')
        sys.exit(2)

    if not CrashPath[-1] == '/':
        CrashPath = CrashPath + '/'
    
    print('Command line = ', Command)
    print('Crash path =', CrashPath)
    print('Output file =', OutputFile)
    print('')        


    # 打印 返回值args列表，即其中的元素是那些不含'-'或'--'的参数。
    for i in range(0, len(args)):
        print('参数 %s 为：%s' % (i + 1, args[i]))


    # start

    # 写之前，先检验文件是否存在，存在就删掉
    if os.path.exists(OutputFile):
        os.remove(OutputFile)

    filelist=[]
    file_name(CrashPath, filelist)
    UniqueSet = set(filelist)
    UniqueList = list(UniqueSet)
    UniqueList.sort()

    os.popen("echo '\n@@@@@@@@@@@@@@@@@@@@@@@@@@     Start    @@@@@@@@@@@@@@@@@@@@@@@@@@\n'" + " > log.txt", 'r')  

    for eachfile in UniqueList:

        os.popen("echo '----------------- go on -------------------'" + " >> " + OutputFile, 'r')
        os.popen("echo 'Commond Line: " + Command + eachfile + "\n'" + " >> " + OutputFile, 'r')
        os.popen("echo 'File Name: " + eachfile + "\n'" + " >> " + OutputFile, 'r')
        os.system(Command + ' ' + eachfile + ' 2>> ' + OutputFile)
        time.sleep(0.01)
        print("Finished: " + eachfile)

    os.popen("echo '\n@@@@@@@@@@@@@@@@@@@@@@@@@@ Finished All @@@@@@@@@@@@@@@@@@@@@@@@@@\n'" + " >> " + OutputFile, 'r')
    time.sleep(0.01)


    print("\nFinished: ALL")

    # end


def file_name(path, filelist): 
    for i in os.walk(path):
        for each in i[2]:
            if "README" not in each:
                filelist.append(path + each)
	
if __name__ == "__main__":
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以用sys.argv[1:]过滤掉脚本名。
    starttime = datetime.datetime.now()

    # print ("\nstart time: ", starttime)

    main(sys.argv[1:])
    
    endtime = datetime.datetime.now()
    
    # print ("start time: ", starttime)
    # print ("end time: ", endtime)

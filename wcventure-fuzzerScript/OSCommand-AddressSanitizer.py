import os
import time

command = './nm/nm -C'
path0 = '/media/hjwang/01D3344861A8D2E0/wcventure/Project/UAF/POC/nm/nm_out/m/crashes/'
path1 = '/media/hjwang/01D3344861A8D2E0/wcventure/Project/UAF/POC/nm/nm_out/s1/crashes/'
path2 = '/media/hjwang/01D3344861A8D2E0/wcventure/Project/UAF/POC/nm/nm_out/s2/crashes/'
path3 = '/media/hjwang/01D3344861A8D2E0/wcventure/Project/UAF/POC/nm/nm_out/s3/crashes/'

def file_name(path, filelist): 
    for i in os.walk(path):
        for each in i[2]:
            if "README" not in each:
                filelist.append(path + each)



# main
filelist=[]
file_name(path0, filelist)
file_name(path1, filelist)
file_name(path2, filelist)
file_name(path3, filelist)
filelist.sort()

os.system("echo '\n@@@@@@@@@@@@@@@@@@@@@@@@@@     Start    @@@@@@@@@@@@@@@@@@@@@@@@@@\n'" + " > log.txt")  

for eachfile in filelist:

    os.system("echo '----------------- go on -------------------'" + " >> log.txt")
    os.system("echo 'Commond Line: " + command + eachfile + "\n'" + " >> log.txt")
    os.system("echo 'File Name: " + eachfile + "\n'" + " >> log.txt")
    os.system(command + ' ' + eachfile + ' 2>> log.txt')
    time.sleep(0.01)
    print("Finished: " + eachfile)

os.system("echo '\n@@@@@@@@@@@@@@@@@@@@@@@@@@ Finished All @@@@@@@@@@@@@@@@@@@@@@@@@@\n'" + " >> log.txt")
time.sleep(0.01)


print("\nFinished: ALL")

# Fuzzing Experimental Data Processing Script

This repository is for Automatic processing Fuzzing Experimental Data.

### Auto capture program status

    CaptureFuzzerStats.py -t <TargetFile> -o <OutputPath> -d <DelayTime>
    CaptureFuzzerStats2.py -t <TargetFile1> -o <OutputPath1> -T <TargetFile2> -O <OutputPath2> -d <DelayTime>
    ExtractCrashesInOrder.py -f <TargetFolder>

### Run the Program with crash, Then classify

Automatically Run The Command Line Program with the crashes input, then output the log with ASAN warning.

    RunCrash.py -c <CommandLine> -i <CrashFolder> -o <OutputFile>

### Run the program with /usr/bin/time -v

    //put the Script in the root folder of the Fuzzing output Folder, then run the Script
    GetRSSInOrder.py -c <CommandLine> -f <TargetFolder>

### Classifying Crashes

    CfyCrashes.py -i <logFile>
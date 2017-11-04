# coding: utf-8

import base64
import os
import sys

handle_list = []


def transfer(path):
    global sucC
    global errC
    try:
        with open(path, 'rb') as f:
            if getSize(f) > 5000:
                print('File:', path)
                print('[+]ERROR: Too large to transfer.')
                errC += 1
            else:
                print('File:', os.path.basename(path))
                b64Str = base64.b64encode(f.read()).decode('utf-8')
                print(b64Str)
                os.system("echo " + b64Str + "| clip")
                sucC += 1
    except IOError as e:
        errC += 1
        print("[+]ERROR!", e)


def getSize(file):
    return os.path.getsize(file.name)


def readTree(path):
    try:
        for file in os.listdir(path):
            if os.path.isdir(file):
                readTree(file)
            if os.path.splitext(file)[1] == ".png":
                handle_list.append(os.path.realpath(file))
        for file in handle_list:
            transfer(file)
    except FileNotFoundError as e:
        getHelp(e)
        sys.exit(2)


def getHelp(err=None):
    if err:
        print(err)
    print('Help: python base.py [path1 [path2 [path3...]]]\nThe last base64 string will be pasted automatically.')


if __name__ == '__main__':
    sucC = errC = 0
    args = sys.argv[1:]
    if len(args) == 0:
        getHelp("Cannot find the path specified.\n")
        sys.exit(1)
    if args[0] == "-h" or args[0] == "--help":
        getHelp()
        sys.exit(1)
    count = 0
    if args[0] == "all":
        readTree(os.getcwd())
    else:
        for path in args:
            count += 1
            transfer(path)
    print(
        'Total:' + (str(count) if count else str(len(handle_list))) + '.\nFail:' + str(errC) + ',Success:' + str(sucC))

#! /usr/bin/env python3
#######################################################################
# File Name: ascii.py
# Author:Justin
# mail:justin13wyx@gmail.com
# Created Time: Sun Dec  3 14:50:30 2017
# ==============================================================
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        char = sys.argv[1]
        res = ord(char)
        print(res)
        

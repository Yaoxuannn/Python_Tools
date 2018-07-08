#! /usr/bin/env python3
#######################################################################
# File Name: unicode.py
# Author:Justin
# mail:justin13wyx@gmail.com
# Created Time: Sun Dec  3 14:50:30 2017
# ==============================================================
import sys, getopt

if __name__ == "__main__":
    reverse = 0
    try:
        opts, argv = getopt.getopt(sys.argv[1:], "r", ["reverse"])
    except getopt.GetoptError:
        print("Bad param.")
        exit(-1)

    for val in opts:
        val = val[0]
        if val in ["-r", "--reverse"]:
            reverse = 1

    try:
        ques = argv[0][0]
        try:
            int(ques)
        except ValueError:
            if reverse == 0:
                print(ord(ques))
                exit(0)
            else:
                print("I guess you don't need -r|--reverse flag.")
                exit(-3)
        if int(ques) > 9 and reverse == 0:
             print("I guess this is code but you don't give the -r|--reverse flag.\nMay check it again?")
             exit(-3)
    except IndexError:
        print("Miss question.")
        exit(-2)

    print("{}".format(chr(int(ques)) if reverse else ord(ques)))

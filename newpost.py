#! /e/Python36/python

import sys, os
from datetime import datetime

working_directory = "D:\\Blog\\source\\_posts"

pattern = '''---
title: {}
date: {}
tags: {}
---

<!--more-->

'''

if __name__ == '__main__':
    os.chdir(working_directory)
    if len(sys.argv) < 3:
        print("missing arguments!")
        exit(-1)
    title = sys.argv[1]
    tags = sys.argv[2].split(",")
    pattern = pattern.format(title, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(tags).replace("'", ""))
    filename = os.path.join(os.getcwd(), "{}.md".format(title))
    f = open(filename, "w", encoding='utf-8')
    f.write(pattern)
    f.close()
    print("New post!")
    os.startfile(filename)
    

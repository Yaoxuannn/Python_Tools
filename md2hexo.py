# coding: utf-8

import os
import sys
import time
import shutil
import datetime
import threading
from configparser import ConfigParser

'''
A simple tool to format markdown for Hexo
'''

handle_list = []

def getInfo():
	md_title = input("title? \n")
	md_date = input("date? example: YYYY-MM-DD hh:mm:ss\n")
	md_tags = input("tags? example: [tag1, tag2, ...]\n")
	md_cate = input("category? \n")
	md_info = '''
---
title: {0}
date: {1}
tags: {2}
---
'''.format(md_title, md_date, md_tags)
	return md_info

def logger(verb):
	timeFmt = '%Y-%m-%d %H:%M:%S'
	curTime = datetime.datetime.now().strftime(timeFmt)
	print("[%s] %s" % (curTime, verb))
	time.sleep(0.5)


def readTree(path):
	cf = ConfigParser()
	cf.read("./md2hexo.conf")
	depth = cf.getint("main", "Maximum_recursion_depth")
	for file in os.listdir(path):
		if depth:
			if os.path.isdir(file):
				depth -= 1
				readTree(file)
		if os.path.splitext(file)[1] == ".md":
			handle_list.append(file)

def handler():
	cf = ConfigParser()
	cf.read("./md2hexo.conf")
	post_path = cf.get("main", "_post_path")
	tmp_dir = os.path.join(post_path if post_path else os.getcwd(), "~tmp")
	os.mkdir(tmp_dir)
	for md in handle_list:
		logger("Handle file: %s" % md)
		bak_path = os.path.join(tmp_dir, "{0}{1}".format("~", md))
		shutil.copyfile(md, bak_path)
		md_info = getInfo()
		new_f = open(md, "w", encoding="utf-8")
		new_f.write(md_info)
		old_f = open(bak_path, "r", encoding="utf-8")
		for lines in old_f:
			new_f.write(lines)

	logger("All done !")
	logger("Summary: %s file handled." % str(len(handle_list)))

def first_run(sure):
	if not sure:
		return
	logger("This is a simple tool to format markdown for Hexo.")
	logger("Please execute this py under your _post directory for \
		this tool will select the current directory as the default work directory")
	logger("Or you can write your _post path in the md2hexo.conf under the curDir")
	logger("This tool just support Python 3.X.")
	logger("The instruction above just appear if this is your first run.")
	# logger("To see the instruction, you can run it with '-h'")

def configer():
	if os.path.isfile("./md2hexo.conf"):
		return False
	cf = ConfigParser()
	cf.add_section("main")
	cf.set("main", "_post_path", "")
	cf.set("main", "Maximum_recursion_depth", "0")
	with open("./md2hexo.conf", "w") as f:
		cf.write(f)

def main():
	first_run(configer())
	logger("Current directory: %s" % os.getcwd())
	logger("Reading the file tree...")
	readingT = threading.Thread(target = readTree, args = (os.getcwd(),))
	readingT.start()
	readingT.join()
	handler()

if __name__ == '__main__':
	main()
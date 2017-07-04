# coding: utf-8

import os
import sys
import time
import shutil
import datetime
import threading
from configparser import ConfigParser

__author__ = "WWW"

'''
A simple tool to format markdown for Hexo
'''

handle_list = []

def getInfo(name):
	md_title = input("title: (last filename default)")
	md_date = input("date(example: YYYY-MM-DD hh:mm:ss): ")
	md_cate = input("category: ")
	md_tags = input("tags(example: [tag1, tag2, ...]): ")
	md_info = '''---
title: {0}
date: {1}
category: {2}
tags: {3}
---'''.format(md_title if md_title else name, md_date if md_date else timeformatter(), md_cate, md_tags)
	return md_info

def logger(verb):
	curTime = timeformatter()
	print("[%s] %s" % (curTime, verb))
	time.sleep(0.1)

def timeformatter():
	timeFmt = '%Y-%m-%d %H:%M:%S'
	curTime = datetime.datetime.now().strftime(timeFmt)
	return curTime

def readTree(path):
	cf = ConfigParser()
	cf.read("./md2hexo.conf")
	depth = cf.getint("main", "Maximum_recursion_depth")
	for file in os.listdir(path):
		if depth:
			if os.path.isdir(file) and not file.startswith("~tmp"):
				depth -= 1
				readTree(file)
		if os.path.splitext(file)[1] == ".md":
			handle_list.append(file)

def handler():
	cf = ConfigParser()
	cf.read("./md2hexo.conf")
	post_path = cf.get("main", "_post_path")
	tmp_dir = os.path.join(post_path if post_path else os.getcwd(), "~tmp")
	if not os.path.exists(tmp_dir):
		os.mkdir(tmp_dir)
	for md in handle_list:
		logger("Handle file: %s" % md)
		bak_path = os.path.join(tmp_dir, "{0}{1}".format("~", md))
		shutil.copyfile(md, bak_path)
		md_info = getInfo(md[:-3])
		new_f = open(md, "w", encoding="utf-8")
		new_f.write(md_info)
		new_f.write("\r\n")
		old_f = open(bak_path, "r", encoding="utf-8")
		for lines in old_f:
			new_f.write(lines)

	logger("All done !")
	logger("Summary: %s file handled." % str(len(handle_list)))

def first_run(sure):
	if not sure:
		return
	# 被老板骂了, 5555...
	# logger("This is a simple tool to format markdown for Hexo.")
	# logger("Please execute this py under your _post directory for this tool will select the current directory as the default work directory")
	# logger("Or you can write your _post path in the md2hexo.conf under the curDir")
	# logger("This tool just support Python 3.X.")
	# logger("The instruction above just appear if this is your first run.")

def configer():
	if os.path.isfile("./md2hexo.conf"):
		return False
	hexo_path = input("Please enter your hexo/source/_post location.[Enter for null]")
	cf = ConfigParser()
	cf.add_section("main")
	cf.set("main", "_post_path", hexo_path)
	cf.set("main", "Maximum_recursion_depth", "0")
	with open("./md2hexo.conf", "w") as f:
		cf.write(f)
	return True

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

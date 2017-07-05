# coding: utf-8

import os
import sys
import time
import shutil
import datetime
import threading
from configparser import ConfigParser

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
	try:
		for file in os.listdir(path):
			if depth:
				if os.path.isdir(file) and not file.startswith("~tmp"):
					depth -= 1
					readTree(file)
			if os.path.splitext(file)[1] == ".md":
				handle_list.append(file)
	except FileNotFoundError as e:
		logger("There are some error about your path specified.")
		logger("Here is the detail of your exception: ")
		print(e)
		sys.exit(1)
	
def handler():
	cf = ConfigParser()
	cf.read("./md2hexo.conf")
	post_path = cf.get("main", "_post_path")
	work_path = post_path if post_path else os.getcwd()
	tmp_dir = os.path.join(work_path, "~tmp")
	if not os.path.exists(tmp_dir):
		try:
			os.mkdir(tmp_dir)
		except FileNotFoundError as e:
			logger("There are some error about your path specified.")
			logger("Here is the detail of your exception: ")
			print(e)
			sys.exit(1)
	for md in handle_list:
		logger("Handle file: %s" % md)
		bak_path = os.path.join(tmp_dir, md)
		shutil.copyfile(os.path.join(work_path, md), bak_path)
		md_info = getInfo(md[:-3])
		new_f = open(os.path.join(work_path, md), "w", encoding="utf-8")
		new_f.write(md_info)
		new_f.write("\r\n")
		old_f = open(bak_path, "r", encoding="utf-8")
		isPrim = True
		for lines in old_f:
			if lines.startswith("#") and isPrim:
				isPrim = False
				continue
			new_f.write(lines)
		get_confirm = False
	while not get_confirm:
		last_order = input("Delete backup folder ~tmp?(yes/no)\n")
		if last_order == 'y' or last_order == 'Y':
			print("You should type exact 'yes' to confirm.\n")
			get_confirm = False
		elif last_order == 'yes':
			shutil.rmtree(tmp_dir)
			get_confirm = True
		elif last_order	!= 'yes':
			get_confirm = True
	logger("All done !")
	logger("Summary: %s file handled." % str(len(handle_list)))

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
	configer()
	cf = ConfigParser()
	cf.read("./md2hexo.conf")
	post_path = cf.get("main", "_post_path")
	logger("Current directory: %s" % post_path if post_path else os.getcwd())
	logger("Reading the file tree...")
	readingT = threading.Thread(target = readTree, args = (post_path if post_path else os.getcwd(),))
	readingT.start()
	readingT.join()
	handler()

if __name__ == '__main__':
	main()

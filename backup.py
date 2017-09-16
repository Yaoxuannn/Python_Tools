# coding: utf-8
import difflib
import json
import multiprocessing
import os
import shutil
import sys

CONFIG_PATH = os.path.join(os.getcwd(), "backup.conf")
POOL_CAPACITY = 0
pool = None
SOURCE_DIR = ""
DEST_DIR = ""
FILTER = []

default_config = '''
{
    "processes":"5",
    "source":"",
    "destination":"",
    "filter":"[.md]"
}
'''


# 首先读取配置文件,没有则创建. 初始化进程池, 读取文件夹, 确定存在性, 接着进行文件迁移.
# 文件迁移时, 先进行diff对比, 如果没有发生改变, 则跳过.

def try_config():
    if not os.path.exists(CONFIG_PATH):
        init_config()
    conf = open(CONFIG_PATH, encoding="utf-8")
    config = json.load(conf)
    POOL_CAPACITY = min(config['processes'], 10)
    SOURCE_DIR = config['source']
    DEST_DIR = config['destination']
    FILTER = config['filter']
    conf.close()


def init_config():
    with open(CONFIG_PATH, mode="w", encoding="utf-8") as f:
        f.write(default_config)


def config():
    global pool
    pool = multiprocessing.Pool(processes=POOL_CAPACITY)
    check_path(SOURCE_DIR)
    check_path(DEST_DIR)


def check_path(path):
    path = os.path.realpath(path)
    if path == "":
        sys.exit(1)
    if not os.path.exists(path):
        print("%s does not exist.Check your config file out." % path)
        ans = input("Do you want to create %s ?  (Default is y)[ y/n ]" % os.path.basename(path))
        if ans or ans == "y":
            # 创建文件夹
            os.mkdir(path)
        else:
            sys.exit(2)


def check_file(file):
    dest_file = os.path.join(DEST_DIR, file)
    src_file = os.path.join(SOURCE_DIR, file)
    dest_context = open(dest_file, encoding="utf-8").readlines()
    src_context = open(src_file, encoding="utf-8").readlines()
    if os.path.exists(dest_file):
        diff = difflib.context_diff(dest_context, src_context)
        try:
            next(diff)
        except StopIteration:
            return False
    return True


def backup(file):
    src = os.path.join(SOURCE_DIR, file)
    des = os.path.join(DEST_DIR, file)
    res = check_file(file)
    if res:
        shutil.copyfile(src, des)


def read_fs():
    all_file = os.listdir(SOURCE_DIR)
    files = []
    print("Reading filesystem...")
    for file in all_file:
        if os.path.splitext(file)[1] in FILTER:
            files.append(file)
    return files


def main():
    try_config()
    config()
    files = read_fs()
    for file in files:
        pool.apply_async(backup, (file,))
    pool.close()
    pool.join()
    print("All done.")


if __name__ == '__main__':
    main()

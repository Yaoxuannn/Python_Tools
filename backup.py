# coding: utf-8
import filecmp
import json
import multiprocessing
import os
import shutil
import sys

CONFIG_PATH = os.path.join(os.getcwd(), "backup.conf")

default_config = '''{
    "processes":"5",
    "source":"",
    "destination":"",
    "filter":""
}
'''


# 首先读取配置文件,没有则创建. 初始化进程池, 读取文件夹, 确定存在性, 接着进行文件迁移.
# 文件迁移时, 先进行diff对比, 如果没有发生改变, 则跳过.

def try_config():
    if not os.path.exists(CONFIG_PATH):
        init_config()
    conf = open(CONFIG_PATH, encoding="utf-8")
    config = json.load(conf)
    custom_config = {'processes': min(int(config['processes']), 10), 'source': config['source'],
                     'destination': config['destination'], 'filter': config['filter'].split(",")}
    conf.close()

    return custom_config


def init_config():
    with open(CONFIG_PATH, mode="w", encoding="utf-8") as f:
        f.write(default_config)


def check_path(path):
    if not path:
        print("You haven't complete your conf file.")
        sys.exit(1)
    if not os.path.exists(path):
        print("%s does not exist.Check your config file out." % path)
        ans = input("Do you want to create %s ?  (Default is y)[ y/n ]" % os.path.basename(path))
        if ans or ans == "y":
            # 创建文件夹
            os.mkdir(path)
        else:
            sys.exit(2)


def check_file(file, src, dest):
    dest_file = os.path.join(os.path.realpath(dest), file)
    src_file = os.path.join(os.path.realpath(src), file)
    if os.path.exists(dest_file):
        print("%s has already existed." % file)
        return filecmp.cmp(dest_file, src_file)
    return False


def backup(file, config):
    src = os.path.join(config['source'], file)
    des = os.path.join(config['destination'], file)
    print("Handle file: %s" % file)
    res = check_file(file, config['source'], config['destination'])
    if not res:
        shutil.copyfile(src, des)


def read_fs(src, _filter):
    all_file = os.listdir(src)
    files = []
    print("Reading filesystem...")
    if _filter == ['']:
        return all_file
    for file in all_file:
        if os.path.splitext(file)[1] in _filter:
            files.append(file)
    return files


def main():
    config = try_config()
    files = read_fs(config['source'], config['filter'])
    pool = multiprocessing.Pool(processes=min(len(files), config['processes']))
    for file in files:
        pool.apply_async(backup, (file, config,))
    pool.close()
    pool.join()
    print("All done.")


if __name__ == '__main__':
    main()

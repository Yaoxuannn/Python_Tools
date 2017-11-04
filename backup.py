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
    "filter":"py:md",
    "delimiter":":"
}
'''


# Return Code:
# 1:  Haven't configure the target in the configure file.
# 2:  Cannot find the destination folder, or you disagree to create it.
# 3:  Illegal symbols found in the configure file.
# 4:  None of files found in the source folder.


def try_config():
    if not os.path.exists(CONFIG_PATH):
        init_config()
    conf = open(CONFIG_PATH, encoding="utf-8")
    try:
        config = json.load(conf)
    except json.decoder.JSONDecodeError:
        print("Your path specified has illegal symbols.\nTip: you need use '/' but not '\\'.")
        sys.exit(3)
    custom_config = {'processes': min(int(config['processes']), 20), 'source': config['source'],
                     'destination': config['destination'],
                     'filter': config['filter'].split(config["delimiter"])}
    conf.close()
    return custom_config


def init_config():
    with open(CONFIG_PATH, mode="w", encoding="utf-8") as f:
        f.write(default_config)


def check_path(path):
    if not path:
        print("Please complete your backup.conf first")
        sys.exit(1)
    if not os.path.exists(path):
        print("%s does not exist.Check your config file out." % path)
        ans = input("Do you want to create %s ?  (Default is y)[ y/n ]" % os.path.basename(path))
        if not ans or ans == "y":
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


def backup(file, config, result):
    src = os.path.join(config['source'], file)
    des = os.path.join(config['destination'], file)
    print("Handle file: %s" % file)
    res = check_file(file, config['source'], config['destination'])
    if not res:
        shutil.copyfile(src, des)
        result += 1


def read_fs(src, _filter):
    if not src:
        print("Check your backup.conf")
        sys.exit(1)
    all_file = os.listdir(src)
    files = []
    print("Reading filesystem...")
    if _filter == ['']:
        return all_file
    for file in all_file:
        if file.split(".")[-1] in _filter:
            files.append(file)
    return files


def report(result, sum):
    print("==" * 10)
    print("Report: %s files in requested folder, %s newly updated." % (sum, result))


def main():
    config = try_config()
    check_path(config['destination'])
    files = read_fs(config['source'], config['filter'])
    if not files:
        print("Empty directory.")
        sys.exit(4)
    pool = multiprocessing.Pool(processes=min(len(files), config['processes']))
    result = 0
    for file in files:
        pool.apply_async(backup, (file, config, result))
    pool.close()
    pool.join()
    print("All done.")
    report(result, len(files))


if __name__ == '__main__':
    main()

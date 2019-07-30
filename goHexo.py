#! /e/Python36/python
# coding: utf-8
# This script is written to finish following workflow:
# -Generate and update hexo
# -Copy file to post_bak
# -Git commit and push

import filecmp
import json
import multiprocessing
import os
import shutil


conf = {
    "processes": "5",
    "source": "D:\\Blog\\source\\_posts",
    "destination": "D:\\BlogBackup\\post_bak",
    "filter": "md",
    "delimiter": ":"
}


class CPobj:
    def __init__(self,):
        self.config = {}
        self.filelist= []

    def try_config(self, config):
        '''
        测试config变量合法化, 检测路径是否合法
        :return:
        '''
        self.config = {'processes': min(int(config['processes']), 20), 'source': config['source'],
                         'destination': config['destination'],
                         'filter': config['filter'].split(config["delimiter"])}
        return CPobj.check_path(self.config['destination'])

    @staticmethod
    def check_path(path):
        '''
        测试路径,如不存在询问创建
        :param path:
        :return:
        '''
        if not path:
            return False
        if not os.path.exists(path):
            print("%s does not exist.Check your config file out." % path)
            ans = input("Do you want to create %s ?  (Default is y)[ y/n ]" % os.path.basename(path))
            if not ans or ans == "y":
                os.mkdir(path)
            else:
                return False
        return True

    def backup(self, file):
        '''
        借用shutil类API进行文件复制, 跳过相同文件
        借用filecmp类API进行文件对比,
        比对原理是读取字符串进行内容对比
        :param file:
        :param config:
        :return:
        '''
        src = os.path.join(self.config['source'], file)
        des = os.path.join(self.config['destination'], file)
        if os.path.exists(des):
            if filecmp.cmp(des, src):
                print("[-] %s" % file)
                return
        shutil.copyfile(src, des)
        print("[+] %s" % file)

    def _read_fs(self):
        '''
        读取文件系统,筛选满足条件(后缀)的文件
        存储.
        :return:
        '''
        all_file = os.listdir(self.config['source'])
        files = []
        print("Reading filesystem...")
        if self.config['filter'] == ['']:
            return all_file
        for file in all_file:
            if file.split(".")[-1] in self.config['filter']:
                files.append(file)
        self.filelist = files

    def _report(self, rep):
        print("==" * 10)
        print("Report: %s files in requested folder." % len(self.filelist))
        for file in rep:
            name = file.get()
            if name:
                print(name, "modified.")

    def execute(self):
        '''
        使用自己加载的config进行批量复制
        :return:
        '''
        if not self.config:
            raise ValueError("call try_config first.")
        self._read_fs()
        pool = multiprocessing.Pool(processes=min(len(self.filelist), self.config['processes']))
        rep = []
        for file in self.filelist:
            rep.append(pool.apply_async(self.backup, (file,)))
        pool.close()
        pool.join()
        self._report(rep)


if __name__ == '__main__':
    cpobj = CPobj()
    cpobj.try_config(conf)
    os.chdir("D:\\Blog")
    try:
        os.system("hexo d -g")
    except KeyboardInterrupt:
        print("Byebye")
        exit(1)
    cpobj.execute()


import json
import multiprocessing
import re
from os import path, remove, mkdir
from time import time

import requests
from lxml import etree

URL = "http://node.kg.qq.com/{}?{}={}"
RURL = "http://node.kg.qq.com/cgi/fcgi-bin/kg_ugc_get_homepage"
pool = multiprocessing.Pool(4)
session = requests.Session()

# 最后的一个参数是时间戳(毫秒级)
query = {
    "jsonpCallback": "callback_1",
    "g_tk": "5381",
    "outCharset": "utf-8",
    "format": "jsonp",
    "type": "get_ugc",
    "start": "",
    "num": "8",
    "touin": "",
    "share_uid": "",
    "g_tk_openkey": "5381",
    "_": ""
}

header = {
    "Referer": "",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest"
}


def analyse(url):
    user_pattern = r"http://node.kg.qq.com/(?P<flag>\w+)\?uid=(?P<uid>\w+)\&?.*"
    song_pattern = r"http://node.kg.qq.com/(?P<flag>\w+)\?s=(?P<sid>\w+)\&?.*"
    result = re.match(user_pattern, url, re.X)
    # TODO: 这个地方的实现实在是太丑陋了, 暂时放一下, 日后再想.
    if not result:
        result = re.match(song_pattern, url, re.X)
    if result:
        return result.groupdict()
    print("Analyse error.")
    return None


def fetch_song_list(start, url, uid, result_set):
    header.update({"Referer": url})
    query.update({
        "start": start,
        "share_uid": uid,
        "_": int(round(time() * 1000))
    })
    res = session.get(url, headers=header, params=query)
    data = json.loads(res.text[res.text.index("{"):-1])['data']
    for ugc in data['ugclist']:
        result_set.update({ugc['title']: ugc['shareid']})
    if data['has_more']:
        start += 1
        fetch_song_list(start, url, uid, result_set)
    return result_set


def download_song(key, real_url, location, chunk):
    print("[+] Downloading %s" % key)
    try:
        res = requests.get(real_url, stream=True)
        size = float(res.headers['content-length']) / 1024 / 1024  # 这是左移几位啊...懒得算了
    except requests.ConnectionError:
        print("[-] Network error")
        return False
    ext = "m4a"
    folder = path.join(location, "kg_downloader")
    if not path.exists(folder):
        mkdir(folder)
    st_path = path.join(folder, ".".join([key, ext]))
    written_size = 0
    if path.exists(st_path):
        print("%s already exists." % st_path)
        return False
    try:
        f = open(st_path, "wb")
        for data in res.iter_content(chunk_size=chunk):
            written_size += len(data) / 1024 / 1024
            f.write(data)
            print("[+] Writing data: (%.2fM/%.2fM)  " % (written_size, size), end="\r")
        f.close()
        print("[+] Writing data:  done! :)       ")
        return key
    except (requests.ConnectTimeout, KeyboardInterrupt):
        print("[-] error.")
        exit(-1)
    finally:
        # remove(st_path)
        f.close()


def get_real_pair(song, url):
    res = session.get(url)
    html = etree.HTML(res.text)
    raw_data = html.xpath("/html/body/script[1]/text()")[0]
    title = song if song else html.xpath("/html/head/title/text()")[0].split("-")[0]
    real_url = json.loads(raw_data[raw_data.index("{"):-2])['detail']['playurl']
    return {title: real_url}


def concat_song_url(sid):
    return URL.format("play", "s", sid)


def fetch_data(url, info):
    if info['flag'] == "personal":
        # TODO: 思考更好的方式, 肯定有办法, 这样太丑了
        result_set = {}
        result_set = fetch_song_list(1, RURL, info['uid'], result_set)
        print("[+] Fetch songs list success!!")
        print("[+] Waiting for metadata constructed...(may take a while)")
        for song, sid in result_set.items():
            result_set.update(
                get_real_pair(song, concat_song_url(sid))
            )
        return result_set
    else:
        return get_real_pair("", url)

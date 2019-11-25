#! /usr/bin/env python3
import json
import re
import sys

import requests
import execjs
from Fucking.fuck import dbcache
from Fucking.fuck import fucking_cmd

url = "https://fanyi.baidu.com/v2transapi?from=en&to=zh"
ver = sys.version.split(" ")[0].split(".")[1]
if int(ver) >= 5:
    exception = json.decoder.JSONDecodeError
else:
    exception = ValueError

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/78.0.3904.108 Safari/537.36",
    "Referer": "https://fanyi.baidu.com/",
    "Origin": "https://fanyi.baidu.com",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "X-Requested-With": "XMLHttpRequest",
    "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "dnt": "1"
}

formdata = {
    "from": "en",
    "to": "zh",
    "query": "",
    "transtype": "realtime",
    "simple_means_flag": "3",
    "sign": "",
    "token": ""
}


session = requests.session()


def _fetch_local(keyword):
    local_res = dbcache.lookup(keyword)
    if local_res:
        return prettify(local_res)
    else:
        result = parse_data(keyword, _fetch_data(keyword))
        if not result:
            return False
        dbcache.save(result)
        return result


def prettify(local_data):
    data = local_data[0]
    result = {
        "word": data[0],
        "symbols": data[1],
        "means": data[2]
    }
    result.update({"local": True})
    return result


def fetch(keyword):
    web = fucking_cmd.get_cmd()['force'] | fucking_cmd.get_cmd()['update']
    if web:
        data = _fetch_data(keyword)
        return parse_data(keyword, data)
    else:
        return _fetch_local(keyword)


def _fetch_data(keyword):
    formdata['query'] = keyword
    try:
        s = requests.Session()
        s.get("https://fanyi.baidu.com/")
        r = s.get("https://fanyi.baidu.com/")
        # Get token
        gtk = re.findall(r"window.gtk = '(.*?)';", r.text)[0]
        sign = get_sign(keyword, gtk)
        formdata['sign'] = sign
        formdata.update({
            "token": re.findall(r"token: '(.*?)',", r.text)[0],
        })
        res = s.post(url, data=formdata, headers=header)
    except ConnectionError:
        print("Connection error.")
        return False
    return res.text


def get_sign(word, gtk):
    with open("fuck/cal_sign.js") as f:
        data = f.read()
        sign = execjs.compile(data).call("e", word, gtk)
        return sign


def parse_data(word, data):
    json_dict = json.loads(data)
    if not json_dict['dict_result']:
        return False
    key = json_dict['dict_result']['simple_means']['symbols']
    hassymbol = 'ph_am' in key[0]
    result = {
        "word": word,
        "symbols": str({'美音': key[0]['ph_am'], "英音": key[0]['ph_en']}) if hassymbol else "False",
        "means": str(key[0]['parts']),
        "local": False
    }
    if fucking_cmd.get_cmd()['update']:
        dbcache.save(result)
    return result


def output(result):
    if not result:
        print("You sure your spell is right?")
        exit(-5)
    if result['local']:
        print("From local cache:\t***%s***" % result['word'])
    else:
        print("From Internet:   \t***%s***" % result['word'])
    try:
        symbols = json.loads(result['symbols'].replace("'", "\""))
        for k, v in symbols.items():
            if v:
                sys.stdout.write("%s: [ %s ]\t" % (k, v))
    except exception:
        sys.stdout.write("音标中含有非法字符!")
    print("")
    means = "{\"means\": %s}" % result['means'].replace("\'", "\"")
    print("释义:")
    try:
        means = json.loads(means)['means']
        for mean in means:
            if 'part' in mean:
                print("\t{0:3}   {1}".format(mean['part'], mean['means']))
            elif 'part_name' in mean:
                print("\t来源于网络的结果:   {0}".format(mean['means']))
    except exception:
        print(means)


def main():
    dbcache.init()
    result = fetch(fucking_cmd.parse_cmd())
    output(result)


if __name__ == "__main__":
    main()

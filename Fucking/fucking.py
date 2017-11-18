#! /usr/bin/env python3
import json
import sys

import requests
from Fucking.fuck import dbcache
from Fucking.fuck import fucking_cmd

url = "http://fanyi.baidu.com/v2transapi"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 \
     (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Referer": "http://fanyi.baidu.com/",
    "Origin": "http://fanyi.baidu.com",
    "X-Requested-With": "XMLHttpRequest"
}

formdata = {
    "from": "en",
    "to": "zh",
    "query": "",
    "transtype": "translang",
    "simple_means_flag": "3"
}


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
        res = requests.post(url, data=formdata, headers=header)
    except ConnectionError:
        print("Connection error.")
        return False
    return res.text


def parse_data(word, data):
    json_dict = json.loads(data)
    if not json_dict['dict_result']:
        return False
    key = json_dict['dict_result']['simple_means']['symbols']
    result = {
        "word": word,
        "symbols": str({'美音': key[0]['ph_am'], "英音": key[0]['ph_en']}),
        "means": str(key[0]['parts']),
        "local": False
    }
    if fucking_cmd.get_cmd()['update']:
        dbcache.save(result)
    return result


def output(result):
    if not result:
        print("Your sure your spell is right?")
        exit(-5)
    if result['local']:
        print("From local cache:\t***%s***" % result['word'])
    else:
        print("From Internet:   \t***%s***" % result['word'])
    symbols = json.loads(result['symbols'].replace("'", "\""))
    for k, v in symbols.items():
        if v:
            sys.stdout.write("%s: [ %s ]\t" % (k, v))
    print("")
    means = "{\"means\": %s}" % result['means'].replace("\'", "\"")
    print("释义:")
    for mean in json.loads(means)['means']:
        print("\t{0:3}   {1}".format(mean['part'], mean['means']))

def main():
    dbcache.init()
    result = fetch(fucking_cmd.parse_cmd())
    output(result)

if __name__ == "__main__":
    main()

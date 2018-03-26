import api
import kg_cmder


def main():
    url, loc = kg_cmder.parse_cmd()
    pre_info = api.analyse(url)
    result = []
    if not pre_info:
        print("URL invalid.")
        exit(-1)
    if pre_info['flag'] in ['personal', 'play']:  # 过滤未来全民K歌可能会搞出来的某些神奇的玩意
        result_set = api.fetch_data(url, pre_info)
        print("[+] Construct metadata successful!")
        print("[+] Download all songs to %s..." % loc)
        for key, val in result_set.items():
            result.append(api.download_song(key, val, loc, 1024))
        print("[+] Report:\n%s" % result)
    else:
        # 未知领域哈哈哈
        exit(-2)


if __name__ == '__main__':
    main()

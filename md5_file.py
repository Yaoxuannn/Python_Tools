import hashlib
import sys


def cal_md5(path):
    md5 = hashlib.md5()
    file = open(path, "rb")
    while True:
        frag = file.read(4096)
        if not frag:
            break
        md5.update(frag)
    md5_sum = md5.hexdigest()
    file.close()
    return md5_sum


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("%s:%s" % (sys.argv[1], cal_md5(sys.argv[1])))
    else:
        print("You need give the file path")

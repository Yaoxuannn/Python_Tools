# coding: utf-8
import getopt
import socket
import sys

from .dbcache import get_size

help_info = {
    "fucking word": "Get the pronunciation and the definition of the `word`. \n\t\t\t\t\t(double quotation marks are "
                    "needed if the `word` is a phrase or a sentence)",
    "fucking -f|--force word": "Force to fetch data from the Internet",
    "fucking -u|--update word": "Update the local cache of the `word`(Has the same effect of the -f)",
    "fucking -p|--ping": "Ping the target to check the connection",
    "fucking -s|--size": "Return the current size of the database",
    "fucking -v|--version": "Display the version infomation",
    "fucking -h|--help": "Print this help information"
}
force = 0
update = 0

VERSION = 'fucking: 1.0.6 Written by Justin13\nBug report: justin13wyx@gmail.com'


def get_cmd():
    return {
        "force": force,
        "update": update
    }


def usage():
    m = max(map(len, help_info.keys()))
    print("Usage:")
    for k in help_info:
        print("\t", k.ljust(m), "\t", help_info[k])


def ping():
    try:
        soc = socket.socket()
        res = soc.connect(("fanyi.baidu.com", 80))
        print("Success!")
    except Exception:
        print("Fail!")
    finally:
        soc.close()


def version():
    print(VERSION)


def parse_cmd():
    global force
    global update
    try:
        opts, args = getopt.getopt(sys.argv[1:], "fuphvs", ["size", "version", "help", "update", "force", "ping"])
    except getopt.GetoptError:
        print("Bad parameter.\n")
        usage()
        exit(3)

    for val in opts:
        val = val[0]
        if val in ["-v", "--version"]:
            version()
            exit(0)
        elif val in ["-p", "--ping"]:
            ping()
            exit(0)
        elif val in ["-f", "--force"]:
            force = 1
        elif val in ["-u", "--update"]:
            update = 1
        elif val in ["-s", "--size"]:
            db_size = get_size()
            print(db_size[0], db_size[1])
            exit(0)
        elif val in ["-h", "--help"]:
            usage()
            exit(0)

    try:
        word = args[0]
    except IndexError:
        print("Seems like you lose your word?")
        exit(-2)

    return word

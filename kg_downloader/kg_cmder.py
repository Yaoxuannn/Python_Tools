from getopt import getopt, GetoptError
import sys
from os import getenv


VERSION = 'kg_downloader: 0.1.0 Written by Justin13\nBug report: justin13wyx@gmail.com'

help_info = {
    "kg_downloader [-l|--location] url": "Let kg_downloader analyse the given url and download songs.",
    "kg_downloader -l|--location": "Specify the download path.[default: HOME]",
    "kg_downloader -v|--version": "Display version information.",
    "kg_downloader -h|--help": "Print this help information."
}


def usage():
    m = max(map(len, help_info.keys()))
    print("Usage:")
    for k in help_info:
        print("\t", k.ljust(m), "\t", help_info[k])


def version():
    print(VERSION)


def parse_cmd():
    location = getenv("HOME")
    try:
        opts, args = getopt(sys.argv[1:], "vhl", ["version", "help", "location"])
    except GetoptError:
        print("Bad parameter.\n")
        usage()
        exit(3)
    for val in opts:
        val = val[0]
        if val in ["-v", "--version"]:
            version()
            exit(0)
        elif val in ["-h", "--help"]:
            usage()
            exit(0)
        elif val in ["-l", "--location"]:
            location = args[0]

    if not args:
        print("You miss your url.")
        usage()
        exit(3)
    return args[-1], location


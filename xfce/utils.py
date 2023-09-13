import os
import re
import sys
import urllib.parse as parse_url
from colorama import Fore
from tabulate import tabulate as tab

URL = "https://xfce-look.org"  # The main URL
SEARCH_URL = "https://xfce-look.org/find?"  # The search URL
keys = {
    "id": Fore.MAGENTA + "id" + Fore.RESET,
    "title": Fore.MAGENTA + "title" + Fore.RESET,
    "url": Fore.MAGENTA + "url" + Fore.RESET,
    "pub": Fore.MAGENTA + "publisher" + Fore.RESET,
    "time": Fore.MAGENTA + "date" + Fore.RESET,
    "rate": Fore.MAGENTA + "rate" + Fore.RESET,
    "cat": Fore.MAGENTA + "category" + Fore.RESET,
}
datas = {keys["id"]: [], keys["title"]: [], keys["pub"]: [], keys["time"]: [], keys["cat"]: [], keys["rate"]: [],
         keys["url"]: []}
archive_types = [".zip", ".tar", ".gz", ".tgz", ".bz2", ".7z", ".rar", ".lzma", ".xz", ".lz"]
img_types = [".png", ".jpg", ".jpeg"]


def get_url_query(s=None, p=0):
    q = s or prompt("search")
    if q == "q" or q == "quit":
        quit(0)

    q = q[:15]

    o = {}
    o.update({"search": q})

    if p:
        o.update({"page": str(p)})

    return SEARCH_URL + parse_url.urlencode(o), q


def debug(*args, __l=False, c=1):

    cl = {
        1: Fore.BLUE,
        -1: Fore.MAGENTA,
        0: Fore.RED,
        2: Fore.GREEN
    }.get(c)

    if __l:
        a = ""
        for i in args:
            a += str(i) + " "
        sys.stdout.write("\r " + cl + a + Fore.RESET)
    else:
        print(cl, *args, Fore.RESET)


def format_(__t, __s="", __n=""):
    return __t.replace("\n", __n).replace(" ", __s)


def prompt(__p):
    return input(Fore.BLUE + " " + __p + " >> " + Fore.RESET).lower()


def split(k=30):
    debug("*" * k)


def tabulate(d):
    debug("tabulating (use full-screen for better experience *_*) ...")

    table = tab(d, headers="keys", tablefmt="fancy_outline")
    print(table)


def exception_handler(*args):
    if os.getenv("DEV_END"):
        print(*args)
    debug("good bye !", c=0)


def print_startup_msg():
    header_footer = "*" * 84
    info = [
        "Author: badr-eddin",
        "GitHub: 'https://github.com/badr-eddin'",
        "Repository: 'https://github.com/badr-eddin/xfce-look'",
        "Version: 0.1",
        "This tool allows you to download and set xfce-theme from 'https://xfce-look.org'",
        "Currently supported categories (v0.1):",
        "  - GTK3/4 Themes",
        "  - Full Icon Themes",
        "  - Cursors",
        "  - Wallpapers (png, jpg, jpeg)",
        "Support me at: 'https://www.buymeacoffee.com/badreddin08'"
    ]

    print(header_footer)
    for line in info:
        print("* {:<80} *".format(line))
    print(header_footer)

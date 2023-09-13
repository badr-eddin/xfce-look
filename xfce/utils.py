import os
import urllib.parse as parse_url
from colorama import Fore
from tabulate import tabulate as tab


URL = "https://www.xfce-look.org"  # The main URL
SEARCH_URL = "https://www.xfce-look.org/find?"  # The search URL
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


def get_url_query():
    q = prompt("search")
    if q == "q" or q == "quit":
        quit(0)

    return SEARCH_URL + parse_url.urlencode({"search": q})


def debug(*args):
    print(Fore.BLUE, *args, Fore.RESET)


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
    debug("good bye !")

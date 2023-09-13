import requests
from bs4 import BeautifulSoup
from .utils import get_url_query, debug, format_, keys, Fore, URL


def scrap():
    data = {keys["id"]: [], keys["title"]: [], keys["pub"]: [], keys["time"]: [], keys["cat"]: [], keys["rate"]: [],
            keys["url"]: []}

    url, _q = get_url_query()
    count = 0
    pages = get_pages(url)
    _l = False

    debug(f"getting page [{url}] ...")

    results = []

    for page in range(1, pages+1):
        bs4 = BeautifulSoup(requests.get(get_url_query(_q, page)[0]).content, features="lxml")

        # ------------------------- Searching for item card ----------------------------------
        debug(f"surfing page [{page}/{pages}] ...", __l=not _l)

        results = bs4.find_all("div", class_="explore-product")

        for tag in results:
            a_s = tag.find_all_next("h3")
            text = format_(a_s[0].text)

            if text:
                data[keys["id"]].append(Fore.MAGENTA + str(count + 1) + Fore.RESET)
                data[keys["title"]].append(Fore.YELLOW + text + Fore.RESET)
                data[keys["url"]].append(URL + a_s[0].find_all_next("a")[0]["href"])
                count += 1

            publisher = tag.findAllNext("a", class_="tooltip""user")
            data[keys["pub"]].append(Fore.BLUE + format_(publisher[0].text) + Fore.RESET)

            time_ = tag.findAllNext("div", class_="collected")
            data[keys["time"]].append(Fore.BLUE + format_(time_[0].text, __s=" ") + Fore.RESET)

            rate = tag.findAllNext("div", class_="kkSWyw")
            data[keys["rate"]].append(Fore.BLUE + format_(rate[0].text) + Fore.RESET)

            category = tag.findAllNext("div", class_="title")
            data[keys["cat"]].append(Fore.BLUE + format_(category[0].findAllNext("b")[0].text, __s=" ") + Fore.RESET)

    print()

    return results, data, count


def get_pages(url):
    bs4 = BeautifulSoup(requests.get(url).content, features="lxml")
    pages_html = bs4.find_all("ul", class_="pagination")[0].findAllNext("li")
    pages = 0
    for i in pages_html:
        if format_(i.text).isdigit():
            pages += 1

    return pages

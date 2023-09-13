import requests
from bs4 import BeautifulSoup
from .utils import get_url_query, debug, format_, keys, Fore, URL


def scrap():
    data = {keys["id"]: [], keys["title"]: [], keys["pub"]: [], keys["time"]: [], keys["cat"]: [], keys["rate"]: [],
            keys["url"]: []}

    url = get_url_query()
    count = 0

    debug(f"getting page [{url}] ...")

    bs4 = BeautifulSoup(requests.get(url).content, features="lxml")

    # ------------------------- Searching for item card ----------------------------------
    debug("looking for results ...")

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

    return results, data, count

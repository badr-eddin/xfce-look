from .utils import prompt, debug, Fore, split, keys
import requests
import pathlib
import os
import re
import shutil
import tempfile
import patoolib
import urllib.parse as parse_url
from rich.progress import track
from .utils import archive_types


def get_id_prompt(count):
    while 1:
        selection = prompt(f"select an id [q/quit] [1-{count}]")
        if selection == "quit" or selection == "q":
            return -1
        elif selection.isdigit():
            if int(selection) <= count:
                return int(selection)
            debug(f"enter a valid selection !")
        else:
            debug(f"enter a valid selection !")


def get_stream_files(u):
    jsf = requests.get(u + "/loadFiles").json()
    data_ = {}

    for file in jsf.get("files") or []:
        if file.get("title"):
            data_.update({
                file.get("title"): {
                    "size": file.get("size"),
                    "url": parse_url.unquote(file.get("url") or ""),
                    "active": file.get("active")
                }
            })

    return data_


def print_selection(d):
    split()
    k = d.keys()
    nd = d.copy()
    for i, v in enumerate(k):
        ext = os.path.splitext(v)[1]
        if ext in archive_types:
            print(Fore.MAGENTA, i + 1,
                  Fore.RESET + ": " + Fore.GREEN + v + " |",
                  str(round((int(d[v].get("size") or "0")) / 1024 / 1024)) + "MB", Fore.RESET)
        else:
            del nd[v]

    if not nd:
        debug("no downloads available !")
        split()
        return -1

    split()

    if len(nd.keys()) <= 1:
        n = prompt(f"do you want to continue [yY-nN]")
        if n.lower() == "n":
            return -1
        return 0

    while 1:
        n = prompt(f"which one to install [q/quit] [1-{len(d.keys())}]")
        if n == "quit" or n == "q":
            return -1
        elif n.isdigit():
            if int(n) <= len(d.keys()):
                return int(n) - 1
            debug(f"enter a valid selection !")
        else:
            debug(f"enter a valid selection !")


recursion_counter = 0


def _download(s, r=False):
    global recursion_counter

    tmp = tempfile.mktemp()
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.mkdir(tmp)

    filename = os.path.join(tmp, pathlib.Path(s).name)
    if recursion_counter < 10:
        recursion_counter += 1
        if r:
            debug(f"trying for the {recursion_counter}th time ...")
        try:
            response = requests.get(s, stream=True)
            x = 1024 ** 2
            size = int(response.headers.get('content-length', 0))
            progress_bar = track(response.iter_content(chunk_size=x), " downloading ...", total=size/x)

            with open(filename, 'wb') as f:
                for chunk in progress_bar:
                    f.write(chunk)
            recursion_counter = 0
            return filename
        except Exception as e:
            _ = e
            return _download(s, True)
    else:
        debug("timeout ! try again and make sure you are connected to the network !")
        return -1


def save_xfce_package(p, c):
    # ask user if he wants to save a copy of the package
    dw = os.path.join(os.path.expanduser("~"), "Downloads")

    if not os.path.exists(dw):
        os.mkdir(dw)

    save = prompt(f"do you want to save a copy in {dw} ?")

    if save != "n" and save != "no" and save != "!y" and save != "!yes":
        shutil.copy2(p, dw)

    dst = {
        "GTK3/4 Themes": os.path.join(os.path.expanduser("~"), ".themes"),
        "Full Icon Themes": os.path.join(os.path.expanduser("~"), ".icons"),
        "Cursors": os.path.join(os.path.expanduser("~"), ".icons"),
    }
    dst_ = None
    for d in dst:
        if re.findall(d, c):
            dst_ = dst.get(d)

    if dst_:
        patoolib.extract_archive(p, -1, dst_)
    else:
        shutil.copy2(p, dw)
        debug(f"unrecognized category ! exporting '{os.path.basename(p)}' to '{dw}'")

    # get rid of the whole tmp dir
    shutil.rmtree(os.path.split(p)[0])


def download(data, c):
    while 1:
        s = get_id_prompt(c) - 1
        if s >= 0:
            url_ = data[keys['url']][s]
            split()
            debug(f"getting {data[keys['title']][s]} ...")
            jsd = get_stream_files(url_)
            k = print_selection(jsd)
            if k >= 0:
                obj = jsd[list(jsd.keys())[k]]
                down = _download(obj.get("url"))
                if isinstance(down, int):
                    continue
                else:
                    save_xfce_package(down, data[keys['cat']][s])
        else:
            break

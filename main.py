import os
import sys
import time

from xfce import *

sys.excepthook = exception_handler

os.environ["DEV_END"] = "1"

while 1:
    os.system("clear")
    results, data, count = scrap()
    if len(results):
        tabulate(data)
        download(data, count)
    else:
        debug("no results !")
    time.sleep(0.5)

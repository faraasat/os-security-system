import json
import os
from datetime import datetime

def get_config():
    f = open("oss.config.json")
    return json.load(f)

def absolute_path(dn):
    return os.path.join(os.path.dirname(__file__), dn)

def is_path_valid():
    cache_path = absolute_path(get_config()["log_path"])
    if not os.path.isdir(cache_path):
        os.mkdir(cache_path)

def logger_dir():
    dt = datetime.now()
    dt_name = dt.strftime("%Y-%m-%d_%H-%M-%S-%f")
    is_path_valid()
    os.mkdir(absolute_path(os.path.join(get_config()["log_path"], dt_name)))
    return absolute_path(os.path.join(get_config()["log_path"], dt_name))

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CYELLOW = '\33[33m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CBLINK = '\33[5m'
    UNDERLINE = '\033[4m'

def check_verbosity(msg=""):
    if get_config()["verbosity"] == 1:
        print(msg)
#!/usr/bin/env python3
import os.path
BASE_PATH = '/home/ldform/'
DATA_PATH = os.path.join(BASE_PATH, "lddata")

import sys
sys.path[0] = BASE_PATH

import ldform
ldform.cgi_main(DATA_PATH, traceback=True)

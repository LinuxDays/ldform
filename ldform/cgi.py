#!/usr/bin/env python3

import cgi
import cgitb

import os
import datetime
import random
import string
import json
import importlib

# Python 3.2 compatibility
if __package__ is None:
    __package__ = "ldform"

# Base path global variable
BASE_PATH = ""


class MyDict(dict):
    """
    Dictionary with few convinience functions and
    a default value instead of KeyError
    """
    def getfirst(self, key, default=None):
        return self.get(key, [default])[0]

    def getlist(self, key, default=''):
        return ", ".join(self.get(key, [default]))

    def __missing__(self, key):
        return [""]


def _randstr(length=3):
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase)
                   for i in range(length))


def save(data):
    global BASE_PATH
    outfname = "{}.json".format(data['regid'])
    with open(os.path.join(BASE_PATH, data['formid'], outfname),
              "w", encoding="utf-8") as outf:
        json.dump(data, outf, indent=4, sort_keys=True, ensure_ascii=False)
        outf.write('\n')


def cgi_main(base_path, traceback=False):
    """
    Serve CGI query
    There has to be a formid value with a corresponding data directory.
    A JSON file is produced in target directory with all user submitted
    values plus remote IP address and a nonce, which can be used to
    authenticate the owner of such request.
    Finally a notify and respond functions of module named same as formid
    is called. The intended purpuse is to send e-mail notification and
    create a HTML response output.

    @param base_path path where to store collected form JSONs
                        (subdirectory per formid should exist)
    @param traceback display fancy tracebacks on an exception
    """
    global BASE_PATH
    BASE_PATH = base_path
    if traceback:
        cgitb.enable()

    try:
        form = cgi.FieldStorage()
        formid = os.path.basename(form.getfirst('formid', 'default'))
        outpath = os.path.join(BASE_PATH, formid)
        if not os.path.isdir(outpath) or not os.access(outpath, os.W_OK):
            raise RuntimeError("No valid formid found.")

        data = MyDict()
        for key in form.keys():
            data[key] = form.getlist(key)

        regid = datetime.datetime.now().strftime("%Y%m%d-%H%M%S"
                                                 "-{}".format(_randstr(3)))

        # Make sure these are added after user-supplied input
        # so they can be trusted
        data['formid'] = formid
        data['regid'] = regid
        data['nonce'] = _randstr(10)
        data['ip'] = os.environ["REMOTE_ADDR"]

        try:
            handler = importlib.import_module('.handlers.{}'.format(formid),
                                              __package__)
        except ImportError:
            handler = importlib.import_module('.handlers.generic',
                                              __package__)

        handler.respond(data)
        save(data)

    except RuntimeError as e:
        print("Content-type: text/html; charset=UTF-8")
        print("""
<html>
<body>
<h1>Something went wrong</h1>
<p>We were unable to process your request…</p>
<pre>{}</pre>
</body>
</html>
    """.format(e))

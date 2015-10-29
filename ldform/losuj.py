#!/usr/bin/env python3
import os
import json
import argparse
import sys
import csv
import random

BASE_PATH = '/srv/www/lddata'


def export_data(formid, *args):
    """ Generate list of with values for *args. """
    global BASE_PATH
    path = os.path.join(BASE_PATH, formid)
    for f in sorted(os.listdir(path)):
        if not f.endswith('.json'):
            continue
        with open(os.path.join(path, f), 'r', encoding='utf-8') as inf:
            data = json.load(inf)
        r = []
        for field in args:
            d = data.get(field, [""])
            if type(d) is list:
                r.append(", ".join(d))
            elif type(d) is str:
                r.append(d)
            else:
                r.append("")
        yield r



def main():
    data = list(export_data('fbsun2015', 'name', 'badgeid'))
    winner = random.SystemRandom().choice(data)
    print("\t".join(winner))




if __name__ == '__main__':
    main()

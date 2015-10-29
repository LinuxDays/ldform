#!/usr/bin/env python3
import os
import json
import argparse
import sys
import csv

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


def write_csv(outf, data, dialect='excel-tab', heading=None):
    writer = csv.writer(outf, dialect=dialect)
    if heading:
        writer.writerow(heading)
    writer.writerows(data)

def main():
    parser = argparse.ArgumentParser(description='Export form data'
                                                 'to a CSV file')
    parser.add_argument('-o', '--outfile',
                        help='output to a CSV file instead of stdout')
    parser.add_argument('-n', '--noheader', action='store_true',
                        help='Do not output field names on the first line')
    parser.add_argument('-d', '--dialect', choices=csv.list_dialects(),
                        default='excel-tab', help="CSV dialect to output "
                        "(default %(default)s)")
    parser.add_argument('formid',
                        help="id of form whose data should be extracted")
    parser.add_argument('field', nargs="+",
                        help="list of fields that should be exported")
    args = parser.parse_args()

    data = export_data(args.formid, *args.field)
    heading = None if args.noheader else args.field
    if args.outfile:
        outf = open(args.outfile, 'w', newline='', encoding='utf-8')
    else:
        outf = sys.stdout
    with outf:
        write_csv(outf, data, args.dialect, heading)


if __name__ == '__main__':
    main()

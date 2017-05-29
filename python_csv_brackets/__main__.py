#!/usr/bin/env python

import csv

from sys import argv

from itertools import takewhile, imap

from python_csv_brackets.utils import handle_args, it_consumes, smart_open


def main():
    handle_args()
    csv_kwargs = dict(delimiter=',', quotechar='"')

    with open(argv[1], 'rt') as f0:
        r = csv.reader(f0, **csv_kwargs)
        rows = tuple(imap(
            lambda line: ''.join('{}\0'.format(''.join(takewhile(lambda ch: ch != '(', col))).rstrip()
                                 for col in line), r))

    with smart_open(argv[2]) as f1:
        w = csv.writer(f1, quoting=csv.QUOTE_MINIMAL, **csv_kwargs)
        it_consumes(imap(lambda line: w.writerow(line.split('\0')), rows))


if __name__ == '__main__':
    main()

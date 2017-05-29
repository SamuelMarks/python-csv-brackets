from collections import deque
from itertools import islice
from contextlib import contextmanager
from sys import stdout, stderr, argv
from os import path

from python_csv_brackets import __version__

it_consumes = lambda it, n=None: deque(it, maxlen=0) if n is None else next(islice(it, n, n), None)


@contextmanager
def smart_open(filename=None):
    fh = open(filename, 'wt') if filename and type(filename).__name__ != 'file' else stdout

    try:
        yield fh
    finally:
        if fh is not stdout:
            fh.close()


def handle_args():
    def usage(exit_code=None, extra_msg=None, stream=stderr):
        stream.write('{prog} removes brackets and empty columns from CSV files inplace.\n'
                     'Usage: python {prog} <input_filename> <output_filename>\n'.format(prog=argv[0]))
        if extra_msg is not None:
            stream.write(extra_msg)
        if exit_code is not None:
            exit(exit_code)

    if len(argv) < 2:
        usage(exit_code=1)
    elif argv[1] in ('-h', '--help'):
        usage(stream=stdout, exit_code=0)
    elif argv[1] in ('-v', '--version'):
        usage(extra_msg='{prog} {version}\n'.format(prog=argv[0], version=__version__), exit_code=0)
    elif not path.isfile(argv[1]):
        usage(extra_msg='\nExpected file in first arg, got {}\n'.format(argv[1]), exit_code=2)
    elif len(argv) < 3:
        argv.append(stdout)
    elif argv[2] == '-':
        argv[2] = stdout
    elif not path.isfile(argv[2]):
        usage(extra_msg='\nExpected file in second arg, got {}\n'.format(argv[2]), exit_code=2)

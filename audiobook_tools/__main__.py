# this seems to be the entry point when this module is called like this
# python -m audiobook --help

import sys

from .core import run

def main():     # pragma: no cover
    try:
        run()
    except KeyboardInterrupt:
        sys.exit(1)# create logger 

if __name__ == '__main__':
    main()

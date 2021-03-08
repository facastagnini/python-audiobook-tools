import argparse
import logging
import sys

from . import helpers
from .__version__ import __version__
from .helpers import Audiobook


###################################
# logger - this should be somewhere else....
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
# tmp_directory = tempfile.gettempdir()
# debug_log_file = os.path.join(tmp_directory,'debug.log')
# fh = logging.FileHandler(debug_log_file)
# fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add formatter to fh
# fh.setFormatter(formatter)

# add the handlers to logger
logger.addHandler(ch)
# logger.addHandler(fh)
###################################


def get_hmm():
    """Get a thought.

    >>> get_hmm()
    'hmmm...'
    """
    return "hmmm..."


def hmm():
    """Contemplation...

    >>> hmm()
    hmmm...
    """
    if helpers.get_answer():
        print(get_hmm())


def run():
    """entry point for this module"""

    parser = argparse.ArgumentParser(
        prog="audiobook_tools",
        description="A swiss army knife for audiobook metadata enrich.",
        epilog="Version {version}. [Python {py_major}.{py_minor}.{py_micro}-{platform}] "
        "Source at https://github.com/facastagnini/python-audiobook-tools/".format(
            version=__version__,
            py_major=sys.version_info.major,
            py_minor=sys.version_info.minor,
            py_micro=sys.version_info.micro,
            platform=sys.platform,
        ),
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Enable more verbose messages for debugging"
    )
    parser.add_argument(
        "-t", "--timeout", dest="timeout", type=int, default=10, help="Timeout (seconds) for network requests. Default 10."
    )

    subparsers = parser.add_subparsers(
        title="Available commands", dest="subparser_name", help="To get more help, use the -h option with the command."
    )
    parser_info = subparsers.add_parser(
        "info", description="Get information about an audibook file.", help="Get information about an audiobook file"
    )
    parser_info.add_argument("-f", "--file", type=str, help="audiobook file path")
    parser_info.add_argument(
        "-p",
        "--preserve-original",
        type=bool,
        default=False,
        help="write changes to a new file, preserving the original audiobook.",
    )
    # parser.add_argument('-n', '--dry-run', required=False, help='read only run')

    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    try:
        # test for audiobook file
        args.file
    except AttributeError:
        parser.print_help()
        exit(0)

    ab = Audiobook(args.file)

    print(ab._read_metadata())

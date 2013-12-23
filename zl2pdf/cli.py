# coding=utf8

"""
    zl2pdf.cli
    ~~~~~~~~~~

    this app's command line interface.
"""

from docopt import docopt

from . import __version__
from .zl2pdf import Zl2PDF
from .logger import logger, logging_mapping


__usage__ = """Usage:
  zl2pdf <name> [--pool-size=<pool-size>] [--log-level=<log-level>]
  zl2pdf [-h|-v]

Options:
  -h --help                   show help
  -v --version                show version
  --pool-size=<pool_size>     how many threads to use [default: 20]
  --log-level=<log-level>     logging level from 1 to 6, bigger to logging more [default: 5]

Sample:
  `zl2pdf daily` will port http://zhuanlan.zhihu.com/daily to daily.pdf"""


def main():
    arguments = docopt(__usage__, version=__version__)

    if arguments['<name>']:

        try:
            log_level, pool_size = map(int, [arguments['--log-level'], arguments['--pool-size']])
        except ValueError:
            exit(__usage__)

        logger.setLevel(logging_mapping.get(log_level))

        zl2pdf = Zl2PDF(arguments['<name>'], pool_size=pool_size)
        zl2pdf.run()
    else:
        exit(__usage__)


if __name__ == '__main__':
    main()

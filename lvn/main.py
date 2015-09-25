# Copyright 2015, The Lvn Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import argparse
import logging
import os
import sys

from . import command

# Commands
from . import create
from . import delete
from . import init
from . import list
from . import rename
from . import switch


_logger = logging.getLogger(__name__)


def main():
  global logging

  argparser = argparse.ArgumentParser(description=__doc__)

  argroup = argparser.add_argument_group('Logging')
  argroup.add_argument(
    '--log-level',
    choices=('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'),
    dest='log_level',
    default='INFO',
    help='Logging level. Default: %(default)s')
  argroup.add_argument(
    '--log-format',
    dest='log_format',
    default='%(asctime)s %(levelname)s %(name)s:%(lineno)d: %(message)s',
    help='Format of logging. Default: "%(default)s"')
  argroup.add_argument(
    '--log-config',
    dest='log_config',
    help='Logging config file.')

  command.AddSubcommands(argparser)

  args = argparser.parse_args()

  logging.basicConfig(
    level=args.log_level,
    format=args.log_format)
  if args.log_config:
    import logging.config
    logging.config.fileConfig(
      args.log_config,
      disable_existing_loggers=False)

  args.command_func(args)

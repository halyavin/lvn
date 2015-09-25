# Copyright 2015, The Lvn Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import argparse
import logging
import os

from . import command
from . import lib


_logger = logging.getLogger(__name__)


def ListArgs(subparsers):
  parser = subparsers.add_parser('list', help='List branches')
  parser.set_defaults(command_func=List)


def List(args):
  lvn = lib.GetLvn(os.getcwd())
  for key in lvn.branches:
    if key == lvn.current_branch:
      print '* ' + key
    else:
      print '  ' + key


command.Register(ListArgs)

# Copyright 2015, The Lvn Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import argparse
import logging
import os

from . import command
from . import lib


_logger = logging.getLogger(__name__)


def DeleteArgs(subparsers):
  parser = subparsers.add_parser('delete', help='Delete branch')
  parser.add_argument('branch', help='new branch name')
  parser.set_defaults(command_func=Delete)


def Delete(args):
  lvn = lib.GetLvn(os.getcwd())
  if lvn.current_branch == args.branch:
    _logger.error('Can\'t delete current branch')
    return

  if not lvn.branches.has_key(args.branch):
    _logger.error('Branch doesn\'t exist')
    return

  try:
    lvn.Delete(args.branch)
  finally:
    lvn.Save()


command.Register(DeleteArgs)

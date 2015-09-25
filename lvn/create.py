# Copyright 2015, The Lvn Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import argparse
import logging
import os

from . import command
from . import lib


_logger = logging.getLogger(__name__)


def CreateArgs(subparsers):
  parser = subparsers.add_parser('create', help='Create branch')
  parser.add_argument('branch', help='new branch name')
  parser.add_argument('-d', '--duplicate', action='store_true',
                      help='create a copy of the current branch')
  parser.set_defaults(command_func=Create)


def Create(args):
  lvn = lib.GetLvn(os.getcwd())
  if lvn.branches.has_key(args.branch):
    _logger.error('branch already exists')
    return

  try:
    lvn.SaveCurrentBranch()
    branch = lib.Branch(args.branch)
    lvn.current_branch = args.branch
    lvn.branches[args.branch] = branch
    if not args.duplicate:
      lvn.Revert()
  finally:
    lvn.Save()

command.Register(CreateArgs)

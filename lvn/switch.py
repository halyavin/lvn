# Copyright 2015, The Lvn Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import argparse
import logging
import os

from . import command
from . import lib


_logger = logging.getLogger(__name__)


def SwitchArgs(subparsers):
  parser = subparsers.add_parser('switch', help='Switch to another branch')
  parser.add_argument('branch', help='new branch name')
  parser.set_defaults(command_func=Switch)


def Switch(args):
  lvn = lib.GetLvn(os.getcwd())

  if not lvn.branches.has_key(args.branch):
    _logger.error('branch doesn\'t exist')
    return

  try:
    lvn.SaveCurrentBranch()
    lvn.Revert()
    archive = lvn.SaveNonTracked()
    lvn.Clean()
    lvn.current_branch = args.branch
    lvn.RestoreBranch()
    lvn.RestoreNonTracked(archive)
  finally:
    lvn.Save()


command.Register(SwitchArgs)

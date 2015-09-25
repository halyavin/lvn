# Copyright 2015, The Lvn Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import argparse
import logging
import os

from . import command
from . import lib


_logger = logging.getLogger(__name__)


def RenameArgs(subparsers):
  parser = subparsers.add_parser('rename', help='Rename branch')
  parser.add_argument('branch', help='new branch name')
  parser.set_defaults(command_func=Rename)


def Rename(args):
  lvn = lib.GetLvn(os.getcwd())
  new_branch_name = args.branch
  lvn.RenameBranch(lvn.current_branch, new_branch_name)
  lvn.Save()

command.Register(RenameArgs)

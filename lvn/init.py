# Copyright 2015, The Lvn Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import argparse
import logging
import os
import os.path

from . import command
from . import lib


_logger = logging.getLogger(__name__)


def InitArgs(subparsers):
  parser = subparsers.add_parser('init',
                                 help='Initialize local tools infrastructure')
  parser.set_defaults(command_func=Init)


def Init(args):
  svn_dir = lib.GetSvnDir(os.getcwd())
  lvn_dir = os.path.join(svn_dir, 'lvn')
  if not os.path.isdir(lvn_dir):
    os.mkdir(lvn_dir)
  lvn_file = os.path.join(lvn_dir, 'lvn.json')
  if os.path.exists(lvn_file):
    _logger.error('lvn is already initialized')
    return
  lvn = lib.Lvn()
  lvn.Save(lvn_file)


command.Register(InitArgs)

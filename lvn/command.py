# Copyright 2015, The Lvn Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Program description."""

import argparse
import logging
import sys


_logger = logging.getLogger(__name__)


_CommandArgsFuncs = []


def Register(command_args_func):
  _CommandArgsFuncs.append(command_args_func)


def AddSubcommands(parser):
  subparsers = parser.add_subparsers(help='Subcommands')
  for func in _CommandArgsFuncs:
    func(subparsers)

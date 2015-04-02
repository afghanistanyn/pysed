#!/usr/bin/python
# -*- coding: utf-8 -*-

# arguments.py file is part of pysed.

# Copyright 2014-2015 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# pysed is utility that parses and transforms text

# https://github.com/dslackw/pysed

# Pysed is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
from __metadata__ import (
    __all__,
    __version__,
    __license__,
    __email__
)


def helps():
    """print arguments options"""
    args = [
        "Usage: %s {left}/[pattern]/{right} [input-file]\n" % __all__,
        "Left options:",
        "  s[n]/                search and replace text",
        "  sl[n]/               search and replace in specific line",
        "  l/                   find pattern in each line",
        "Right option:",
        "  /p                   print text",
        "  /w                   write to file\n",
    ]
    for opt in args:
        print opt
    sys.exit(0)


def usage(*args):
    """print arguments usage"""
    msg, option = args
    usg = [
        "usage: {0} [-h] [-v]".format(__all__),
        "             left  [s[n]/, sl[n], l/]",
        "             right [/p, /w]\n"
    ]
    for opt in usg:
        print opt
    if msg in ["left", "right"]:
        print("{0}: error: {1} argument '{2}' is not recognized".format(__all__,
                                                                        msg,
                                                                        option))
    elif msg == "not used":
        print("{0}: error: right argument '{1}' {2}".format(__all__, option,
                                                            msg))
    sys.exit(0)


def optional(args):
    """optional arguments"""
    if len(args) == 1:
        if args[0] in ["-h", "--help"]:
            helps()
        elif args[0] in ["-v", "--version"]:
            print("Version : {0}\n"
                  "License : {1}\n"
                  "Email   : {2}".format(__version__,
                                         __license__,
                                         __email__))
            sys.exit(0)

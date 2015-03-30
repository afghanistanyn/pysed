#!/usr/bin/python
# -*- coding: utf-8 -*-

# main.py file is part of pysed.

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


import re
import sys
from utils import (
    fix_pattern,
    write_file,
    print_file
)

__all__ = "pysed"
__author__ = "dslackw"
__copyright__ = 2014 - 2015
__version_info__ = (0, 5, 0)
__version__ = "{0}.{1}.{2}".format(*__version_info__)
__license__ = "GNU General Public License v3 (GPLv3)"
__email__ = "d.zlatanidis@gmail.com"
__website__ = "https://github.com/dslackw/pysed"


def replace_text(old, new, depth, text):
    """ return replace text """
    find = re.findall(old, text)
    if depth == "":
        depth = len(text)
    if old == "^":
        return ("".join(
            [new + line + "\n" for line in text.splitlines()]).rstrip())
    for p in set(find):
        text = text.replace(p, new, int(depth))
    return text.rstrip()


def find_line(find, text):
    """ find pattern and return lines """
    lines = ""
    for line in text.splitlines():
        if find in line:
            lines += line + "\n"
    return lines.rstrip()


def choice(pattern, text):
    """ return results """
    if len(pattern) == 4:
        if pattern[0].startswith("s"):
            depth = "".join(re.findall(r"\d+", pattern[0]))
            return replace_text(pattern[1], pattern[2], depth, text)
    if len(pattern) == 3:
        if pattern[0].startswith("l"):
            return find_line(pattern[1], text)
    usage()


def options():
    """ print arguments options """
    args = [
        "Usage: %s '{left}/pattern/{right}' [input-file]\n" % __all__,
        "Left options:",
        "  s/           search and replace text",
        "  l/           find pattern and print lines",
        "Right option:",
        "  /p           print text",
        "  /w           write to a file\n",
    ]
    for opt in args:
        print opt
    sys.exit()


def usage():
    """ print arguments usage """
    usg = [
        "usage: {0} [-h] [-v]".format(__all__),
        "             left  [s/, l/]",
        "             right [/p, /w]\n"
    ]
    for opt in usg:
        print opt
    sys.exit()


def arguments(args):
    """ optional arguments """
    if len(args) == 1:
        if args[0] in ["-h", "--help"]:
            options()
        elif args[0] in ["-v", "--version"]:
            print("Version : {0}\n"
                  "License : {1}\n"
                  "Email   : {2}".format(__version__,
                                         __license__,
                                         __email__))
            sys.exit()


def main():
    args = sys.argv
    args.pop(0)
    arguments(args)

    if len(sys.argv) > 1:
        try:
            f = open(args[1])
            data = f.read()
        except IOError:
            print("{0}: error: No such file or directory: {1}".format(__all__,
                                                                      args[1]))
            sys.exit(0)
    else:
        try:
            data = sys.stdin.read()
        except KeyboardInterrupt:
            print("")
            sys.exit()

    # try:
    if len(args) >= 1 and len(args) <= 2:
        pattern = fix_pattern(args[0].split("/"))
        text = choice(pattern, data)

        if len(pattern) == 4:
            option = pattern[3]
            if option == "p":
                print_file(text)
            elif option == "w":
                write_file(text, args[1])
        elif len(pattern) == 3:
            option = pattern[2]
            if option == "p":
                print_file(text)
        else:
            usage()
    else:
        usage()
    # except IndexError:
    #     sys.exit()

if __name__ == "__main__":
    main()

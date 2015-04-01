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


SpecialChars = ["^", "$"]


def checkSpecial(old, new, text):
    """check special characters and return results"""
    if old == "^":
        return ("".join(
            [new + line + "\n" for line in text.splitlines()]).rstrip())
    elif old == "$":
        return ("".join(
            [line + new + "\n" for line in text.splitlines()]).rstrip())


def replaceText(old, new, num, text):
    """return replace tex"""
    find = re.findall(old, text)
    if not num:
        num = len(text)
    if old in SpecialChars:
        return checkSpecial(old, new, text)
    for p in set(find):
        text = text.replace(p, new, int(num))
    return text.rstrip()


def replaceLines(pattern, text):
    """replace specific text in specific lines"""
    nums = pattern[0][2:]
    for n in nums:
        if "," not in n and not n.isdigit():
            usage("left")
        num = nums.split(",")
        old = findLines(num, text)
        for l in text.splitlines():
            for o in old.splitlines():
                if l == o:
                    new = o.replace(pattern[1], pattern[2])
                    if pattern[1] in SpecialChars:
                        new = checkSpecial(pattern[1], pattern[2], new)
                    text = replaceText(l, new, "", text)
        return text
    return replaceText(pattern[1], pattern[2], "", text)


def findPatternLine(find, text):
    """find pattern and return lines"""
    lines = ""
    for line in text.splitlines():
        if find in line:
            lines += line + "\n"
    return lines.rstrip()


def findLines(nums, text):
    """return specific lines"""
    count, lines = 1, ""
    for ln in text.splitlines():
        if str(count) in nums:
            lines += ln + "\n"
        count += 1
    return lines


def options():
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


def arguments(args):
    """optional arguments"""
    if len(args) == 1:
        if args[0] in ["-h", "--help"]:
            options()
        elif args[0] in ["-v", "--version"]:
            print("Version : {0}\n"
                  "License : {1}\n"
                  "Email   : {2}".format(__version__,
                                         __license__,
                                         __email__))
            sys.exit(0)


def executeLeft(pattern, text):
    """executes leftist options and return
       modified text
    """
    if len(pattern) == 4:
        depth = "".join(re.findall(r"\d+", pattern[0]))
        if pattern[0] == "s" or pattern[0][1:].isdigit():
            return replaceText(pattern[1], pattern[2], depth, text)
        elif pattern[0].startswith("sl"):
            return replaceLines(pattern, text)
    elif len(pattern) == 3:
        if pattern[0] == "l":
            return findPatternLine(pattern[1], text)
        else:
            usage("", "")
    if pattern[0] not in ["s", "l"]:
        usage("left", pattern[0])


def executeRight(args, data):
    """executes rightist options and final
       results
    """
    # try:
    if len(args) >= 1 and len(args) <= 2:
        pattern = fix_pattern(args[0].split("/"))
        text = executeLeft(pattern, data)

        if len(pattern) == 4:
            option = pattern[3]
            if option == "p":
                print_file(text)
            elif option == "w":
                write_file(text, args[1])
            else:
                usage("right", option)
        elif len(pattern) == 3 and pattern[2] == "p":
                print_file(text)
        else:
            usage("", "")
    else:
        usage("", "")
    # except IndexError:
    #     sys.exit(0)


def main():
    args = sys.argv
    args.pop(0)
    arguments(args)
    data = ""

    if len(sys.argv) > 1:
        try:
            f = open(args[1])
            data = f.read()
        except IOError:
            print("{0}: error: No such file or directory: {1}".format(__all__,
                                                                      args[1]))
            sys.exit(0)
    elif len(sys.argv) == 1:
        try:
            data = sys.stdin.read()
        except KeyboardInterrupt:
            print("")
            sys.exit(0)
    executeRight(args, data)

if __name__ == "__main__":
    main()

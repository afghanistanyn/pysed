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
    write_file,
    print_file
)
from arguments import (
    usage,
    optional
)
from __metadata__ import (
    __all__,
    specialChars
)
from pattern import Pattern


def checkSpecial(old, new, text):
    """check special characters and return results"""
    if old == "^":
        return ("".join(
            [new + line + "\n" for line in text.splitlines()]).rstrip())
    elif old == "$":
        return ("".join(
            [line + new + "\n" for line in text.splitlines()]).rstrip())


def findPatternLine(find, text):
    """find pattern in lines"""
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


def replaceLines(pattern, text):
    """replace specific text in specific lines"""
    nums = pattern[0][2:]
    for n in nums:
        if "," not in n and not n.isdigit():
            usage("left", pattern[0])
        num = nums.split(",")
        old = findLines(num, text)
        for l in text.splitlines():
            for o in old.splitlines():
                if l == o:
                    new = o.replace(pattern[1], pattern[2])
                    text = replaceText(l, new, text)
        return text
    return replaceText(pattern[1], pattern[2], text)


def replaceText(pattern, new, text):
    """return replace text"""
    return re.sub(pattern, new, text)


def executeLeft(pattern, text):
    """executes leftist options and return
       modified text
    """
    if pattern[1] in specialChars:
        return checkSpecial(pattern[1], pattern[2], text)
    if len(pattern) == 4:
        if pattern[0] == "s":
            return replaceText(pattern[1], pattern[2], text)
        elif pattern[0].startswith("sl"):
            return replaceLines(pattern, text)
        elif pattern[0] == "l":
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
        pattern = Pattern(args[0]).Split()
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
    optional(args)
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

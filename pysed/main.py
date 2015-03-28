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


def write_file(text, reg):
    """ write a new file """
    with open(reg, "w") as f:
        for line in text.splitlines():
            f.write(line + "\n")
        f.close()


def print_file(text):
    """ print text """
    for line in text.splitlines():
        print("{0}".format(line))


def replace_text(old, new, text):
    """ return replace text """
    find = re.findall(old, text)
    for p in find:
        text = text.replace(p, new)
    return text.rstrip()


def choice(pattern, reg):
    """ return results """
    if len(pattern) == 4:
        if pattern[0].startswith("s"):
            return replace_text(pattern[1], pattern[2], reg)
    return ""


def main():
    args = sys.argv
    args.pop(0)

    if len(sys.argv) > 1:
        f = open(args[1])
        data = f.read()
    else:
        try:
            data = sys.stdin.read()
        except KeyboardInterrupt:
            print("")
            sys.exit()
    try:
        if len(args) >= 1 and len(args) <= 2:
            pattern = args[0].split("/")
            text = choice(pattern, data)

            if len(args) == 2:
                option = pattern[3]
                if option == "p":
                    print_file(text)
                elif option == "w":
                    write_file(text, args[1])
            elif len(args) == 1:
                print_file(text)
    except IndexError:
        sys.exit()

if __name__ == "__main__":
    main()

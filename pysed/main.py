#!/usr/bin/env python
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
from __metadata__ import __prog__
from options import (
    usage,
    helps,
    version
)


class Pysed(object):

    def __init__(self, args, data):
        self.args = args
        self.pattern = args[1]
        self.repl = args[2]
        try:
            self.count = int(args[3])
        except ValueError:
            self.count = 0
        self.flag = args[4]
        self.filename = args[5]
        if len(self.args) > 6:
            self.write = args[6]
        self.data = data

    def replaceText(self):
        """replace text with new"""
        newtext = ""
        self.flags()
        for line in self.data.splitlines():
            newtext += re.sub(self.pattern, self.repl, line,
                              self.count, self.flag) + "\n"
        if len(self.args) > 6 and self.write in ["-w", "--write"]:
            self.writeFile(newtext)
        else:
            print(newtext.rstrip())

    def findText(self):
        """find text and print"""
        self.flags()
        for line in self.data.splitlines():
            find = re.search(self.pattern, line, self.flag)
            if find:
                print(line.rstrip())

    def flags(self):
        patt_flag = ""
        for i in self.flag.split("|"):
            re_patt = {
                "I": "re.I",
                "L": "re.L",
                "M": "re.M",
                "S": "re.S",
                "U": "re.U",
                "X": "re.X",
                "0": "0",
                "": ""
            }
            try:
                patt_flag += re_patt[i] + "|"
            except KeyError:
                usage()
                sys.exit("{0}: error: '{1}' flag doesn't exist".format(
                    __prog__, self.flag))
        if self.flag:
            self.flag = eval(patt_flag[:-1])
        else:
            self.flag = 0

    def writeFile(self, newtext):
        """write data to file"""
        with open(self.filename, "w") as fo:
            for line in newtext.splitlines():
                fo.write(line + "\n")
            fo.close()


def execute(args, data):
    if args[0] in ["-r", "--search-repl"]:
        Pysed(args, data).replaceText()
    elif args[0] in ["-s", "--search"]:
        Pysed(args, data).findText()


def main():
    args = sys.argv
    args.pop(0)
    data = ""
    if args and args[0] in ["-h", "--help"]:
        helps()
    elif args and args[0] in ["-v", "--version"]:
        version()
    elif args and args[0] not in ["-h", "--help", "-v" "--version", "-r",
                                  "--search-repl", "-s", "--search"]:
        usage()
        sys.exit("{0}: error: '{1}' argument doesn't exist".format(__prog__,
                                                                   args[0]))

    if len(args) > 5:
        fileInput = args[5]
        try:
            f = open(fileInput)
            data = f.read()
        except IOError:
            usage()
            sys.exit("{0}: error: No such file or directory '{1}'".format(
                __prog__, args[5]))
    else:
        try:
            data = sys.stdin.read()
        except KeyboardInterrupt:
            print("")
            sys.exit()
    if len(args) > 7:
        usage()
        sys.exit("{0}: error: Too many arguments".format(__prog__))
    execute(args, data)

if __name__ == "__main__":
    main()

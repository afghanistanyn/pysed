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

    def __init__(self, args, data, filename):
        self.args = args
        self.flag = "0"
        self.count = 0
        self.pattern = args[1]
        self.repl = args[2]
        self.filename = filename
        if len(args) >= 4:
            try:
                self.count = int(args[3])
            except ValueError:
                self.count = 0
        if len(args) >= 6:
            self.flag = args[4]
        if len(self.args) > 6:
            self.write = args[6]
        self.color = ""
        self.color_def = "\x1b[0m"
        self.data = data.rstrip()
        self.text = ""

    def replaceText(self):
        """replace text with new"""
        self.flags()
        self.text += re.sub(self.pattern, self.repl, self.data, self.count,
                            self.flag)
        self.selectPrintWrite()

    def findLines(self):
        """find text and print"""
        self.flags()
        for line in self.data.splitlines():
            find = re.search(self.pattern, line, self.flag)
            if find:
                self.text += line + "\n"
        self.selectPrintWrite()

    def highLight(self):
        """highlight text and print"""
        self.colors()
        text = (self.data.replace(
            self.pattern, self.color + self.pattern + self.color_def))
        if len(self.args) > 6 and self.write in ["-w", "--write"]:
            self.writeFile(text)
        else:
            print(text.rstrip())

    def flags(self):
        """python regex flags"""
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

    def colors(self):
        """colors dict"""
        paint = {
            'black': '\x1b[30m',
            'red': '\x1b[31m',
            'green': '\x1b[32m',
            'yellow': '\x1b[33m',
            'blue': '\x1b[34m',
            'magenta': '\x1b[35m',
            'cyan': '\x1b[36m',
            }
        try:
            self.color = paint[self.repl]
        except KeyError:
            usage()
            sys.exit("{0}: error: '{1}' color doesn't exist".format(
                __prog__, self.repl))

    def selectPrintWrite(self):
        if len(self.args) > 6 and self.write in ["-w", "--write"]:
            self.writeFile(self.text)
        else:
            print(self.text.rstrip())

    def writeFile(self, newtext):
        """write data to file"""
        with open(self.filename, "w") as fo:
            for line in newtext.splitlines():
                fo.write(line + "\n")
            fo.close()


def execute(args, data, filename):
    """execute available arguments"""
    if len(args) == 7 and args[6] not in ["-w", "--write"]:
        usage()
        sys.exit("{0}: error: '{1}' argument does not recognized".format(
            __prog__, args[6]))

    pysed = Pysed(args, data, filename)
    if args[0] in ["-r", "--replace"]:
        pysed.replaceText()
    elif args[0] in ["-l", "--lines"]:
        pysed.findLines()
    elif args[0] in ["-g", "--highlight"]:
        pysed.highLight()


def main():
    args = sys.argv
    args.pop(0)
    data = ""
    if len(args) == 1 and args[0] in ["-h", "--help"]:
        helps()
    elif len(args) == 1 and args[0] in ["-v", "--version"]:
        version()
    elif len(args) == 0:
        usage()
        sys.exit("{0}: error: Too few arguments".format(__prog__))
    elif args and args[0] not in ["-r", "--replace", "-l", "--lines",
                                  "-g", "--highlight"]:
        usage()
        sys.exit("{0}: error: '{1}' argument does not recognized".format(
            __prog__, args[0]))

    filename = ""
    not_piping = sys.stdin.isatty()
    if not_piping:
        fileInput = filename = args[len(args) - 1]
        print fileInput
        if fileInput in ["-w", "--write"]:
            fileInput = filename = args[len(args) - 2]
        try:
            f = open(fileInput)
            data = f.read()
        except IOError:
            usage()
            sys.exit("{0}: error: No such file or directory '{1}'".format(
                __prog__, args[len(args) - 1]))
    else:
        try:
            data = sys.stdin.read()
        except KeyboardInterrupt:
            print("")
            sys.exit()

    if len(args) > 7:
        usage()
        sys.exit("{0}: error: Too many arguments".format(__prog__))
    execute(args, data, filename)

if __name__ == "__main__":
    main()

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


def writeFile(fileName, data):
    """write data to file"""
    with open(fileName, "w") as fo:
        for line in data.splitlines():
            fo.write(line + "\n")
        fo.close()


def flags(flag):
    patt_flag = ""
    for i in flag.split("|"):
        re_patt = {
            "I": "re.I",
            "L": "re.L",
            "M": "re.M",
            "S": "re.S",
            "U": "re.U",
            "X": "re.X",
            "": ""
        }
        try:
            patt_flag += re_patt[i] + "|"
        except KeyError:
            sys.exit(0)
    if flag:
        flag = eval(patt_flag[:-1])
    else:
        flag = 0
    return flag


def replaceText(args, data):
    """replace text with new"""
    # flag = args[4]
    newText = ""
    patt, repl, count, flag = args[1], args[2], args[3], args[4]
    flag = flags(flag)
    for line in data.splitlines():
        newText += re.sub(patt, repl, line + "\n", int(count), flag)
    if len(args) == 5 and args[4] in ["-w", "--write"]:
        fileName = args[3]
        writeFile(fileName, newText)
    else:
        print(newText.rstrip())


def findText(args, data):
    """find text and print"""
    patt, flag = args[1], args[4]
    flag = flags(flag)
    for line in data.splitlines():
        find = re.search(patt, line, flag)
        if find:
            print(line.rstrip())


def helps():
    """print help"""
    arguments = [
        "pysed is utility that parses and transforms text\n",
        "Usage: pysed [OPTION] {pattern} {repl} {count} {flag} [input-file]\n",
        "Options:",
        "  -h, --help                   display this help and exit",
        "  -v, --version                print program version and exit",
        "  -r, --search-repl            search and replace text",
        "  -s, --search                 search pattern and print",
        "      --write                  write to file\n"
    ]
    for arg in arguments:
        print("{0}".format(arg))
    sys.exit()


def version():
    print("0.5.0")
    sys.exit()


def execute(args, data):
    if args[0] in ["-r", "--search-repl"]:
        replaceText(args, data)
    elif args[0] in ["-s", "--search"]:
        findText(args, data)


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
        sys.exit("Wrong argument")

    if len(args) > 5:
        fileInput = args[5]
        try:
            f = open(fileInput)
            data = f.read()
        except IOError:
            print("No such file or directory: {0}".format(args[4]))
    else:
        try:
            data = sys.stdin.read()
        except KeyboardInterrupt:
            print("")
            sys.exit()
    if len(args) > 7:
        sys.exit("Too many arguments")
    execute(args, data)

if __name__ == "__main__":
    main()

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

import sys


def main():
    args = sys.argv
    args.pop(0)
    data = ""

    if len(args) > 3:
        fileInput = args[3]
        try:
            f = open(fileInput)
            data = f.read()
        except IOError:
            print("No such file or directory: {0}".format(args[3]))
    else:
        try:
            data = sys.stdin.read()
        except KeyboardInterrupt:
            print("")
            sys.exit()
    if len(args) > 5:
        sys.exit("Too many arguments")
    r = data.replace(args[1], args[2])
    sys.stdout.write(r)

if __name__ == "__main__":
    main()

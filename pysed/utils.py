#!/usr/bin/python
# -*- coding: utf-8 -*-

# utils.py file is part of pysed.

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


def fix_pattern(pattern):
    """ fix pattern len """
    if not pattern[-1]:
        pattern = pattern[:-1]
    return pattern


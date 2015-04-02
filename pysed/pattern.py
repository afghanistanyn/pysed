#!/usr/bin/python
# -*- coding: utf-8 -*-

# pattern.py file is part of pysed.

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


class Pattern(object):
    """pattern manager"""

    def __init__(self, pattern):
        self.pattern = pattern

    def getLeftOption(self):
        """get left option from pattern"""
        left = ""
        for c in self.pattern:
            left += c
            if "/" == c:
                return left

    def getRightOption(self):
        """get right option from pattern"""
        right = ""
        for c in self.pattern[::-1]:
            right += c
            if "/" == c:
                return right[::-1]

    def getPattern(self, pattern):
        """get main pattern"""
        pat, orig = "", ""
        if pattern:
            for j in range(len(pattern)):
                orig += pattern[j]
                if "\\" == pattern[j]:
                    orig += pattern[j+1]
                    pat += pattern[j+1]
                    j += 2
                    continue
                pat += pattern[j]
                if "/" in pattern[j] or len(pattern) == j+1:
                    orig = pattern.replace(orig[:-1], "")
                    return pat[:-1], orig[1:].replace("\\", "")
                j += 1
        return "", ""

    def Split(self):
        """split pattern"""
        left = self.getLeftOption()
        right = self.getRightOption()
        pat = self.pattern.replace(left, "")
        pat = pat.replace(right, "")
        old, new = self.getPattern(pat)
        return left[:-1], old, new, right[1:]

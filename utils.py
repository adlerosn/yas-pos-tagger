#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# Copyright (c) 2017 Adler Neves <adlerosn@gmail.com>
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

flatten = lambda lst: [item for sublist in lst for item in sublist]

def sortedListBinarySearch(lst, item):
    baseLimit = 0
    upperLimit = len(lst)
    current = 0
    while(baseLimit!=upperLimit):
        newCurrent = ((upperLimit-baseLimit)//2)+baseLimit
        if current==newCurrent:
            if lst[current]==item:
                break
            elif lst[baseLimit]==item:
                current = baseLimit
                break
            elif lst[upperLimit]==item:
                current = upperLimit
                break
            else:
                break
        current = newCurrent
        if lst[current]==item:
            break
        elif lst[current]>item:
            upperLimit = current
        else:
            baseLimit = current
    if lst[current]==item:
        return current
    else:
        raise ValueError('not found')

def sortedListBinarySearchNoRaise(lst, item):
    try:
        return sortedListBinarySearch(lst, item)
    except ValueError:
        return -1

def getListItemOr(lst, index, default):
    if index in range(len(lst)):
        return lst[index]
    else:
        return default

def dictToKeypair(d):
    return list(d.items())

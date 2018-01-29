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

with open('unitexable_test/corpus.txt.untagged.txt') as f:
    corpus = [[wrd.strip() for wrd in snt.split(' ') if len(wrd)>0] for snt in f.read().strip().splitlines() if len(snt)>0]
    corpus = '\n\n'.join(['\n'.join(snt) for snt in corpus]).splitlines()

with open('unitexable_test/corpus.txt.tagged.txt') as f:
    tags = f.read().strip().splitlines()

for i, tag in enumerate(tags):
    if len(tag)>0:
        corpus[i]+='/'+tag

with open('unitexable_test/corpus.txt.retagged.txt','w') as f:
    f.write('\n'.join(corpus))

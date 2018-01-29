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

def extractStatistics(seq):
    sizeSentences = len(seq)
    _tokens = ' '.join(seq).split(' ')
    sizeTokens = len(_tokens)
    sizeUniqueTokens = len(set(_tokens))
    return {
        'sentences': sizeSentences,
        'tokens': sizeTokens,
        'uniqueTokens': sizeUniqueTokens
    }

with open('unitexable_train/corpus.txt') as f:
    fc = f.read().strip()

corpus = [' '.join([wrd.split('/')[0] for wrd in snt.splitlines() if len(wrd)>0]) for snt in fc.split('\n\n') if len(snt)>0]
stats = extractStatistics(corpus)

import json

with open('unitexable_train/quick_statistics.json','w') as f:
    f.write(json.dumps(stats,indent=4,sort_keys=True))

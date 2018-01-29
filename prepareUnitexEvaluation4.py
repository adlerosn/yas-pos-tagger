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

with open('unitexable_test/corpus.txt.answersheet.txt') as f:
    answers = [sentence.splitlines() for sentence in f.read().strip().split('\n\n')]

with open('unitexable_test/corpus.txt.retagged.txt') as f:
    guesses = [sentence.splitlines() for sentence in f.read().strip().split('\n\n')]

def extractSentence(seq):
    return ' '.join([s.split('/')[0] for s in seq])

answers_d = {extractSentence(n): n for n in answers}
guesses_d = {extractSentence(n): n for n in guesses}

inBoth = {key for key in set(answers_d.keys()).intersection(set(guesses_d.keys())) if len(key)>0}

answers_final = list()
guesses_final = list()

for key in inBoth:
    answers_final.append(answers_d[key])
    guesses_final.append(guesses_d[key])

with open('unitexable_test/corpus.answers_final.txt','w') as f:
    f.write('\n\n'.join(['\n'.join(sentence) for sentence in answers_final]))

with open('unitexable_test/corpus.guesses_final.txt','w') as f:
    f.write('\n\n'.join(['\n'.join(sentence) for sentence in guesses_final]))

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

statistics = {
    'answers': extractStatistics(answers_d.keys()),
    'guesses': extractStatistics(guesses_d.keys()),
    'testset': extractStatistics(inBoth),
}

import json

with open('unitexable_test/quick_statistics.json','w') as f:
    f.write(json.dumps(statistics,indent=4,sort_keys=True))

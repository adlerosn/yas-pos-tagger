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

import json
from utils import getListItemOr, sortedListBinarySearchNoRaise

def deepTupleConversion(lst):
    if isinstance(lst, list):
        for i, l in enumerate(lst):
            if isinstance(l, list) or isinstance(l, dict):
                lst[i] = deepTupleConversion(l)
        return tuple(lst)
    elif isinstance(lst, dict):
        for k, v in lst.items():
            if isinstance(v, list) or isinstance(v, dict):
                lst[k] = deepTupleConversion(v)
        return lst

with open('unitexable_test/corpus.txt.untagged.txt') as f:
    corpus = [[wrd.strip().lower() for wrd in snt.split(' ') if len(wrd)>0] for snt in f.read().strip().splitlines() if len(snt)>0]

print('readed corpus')

with open('unitexable_test/traindata.json') as f:
    taggerData = json.loads(f.read())

deepTupleConversion(taggerData)

tagset = taggerData['tagset']
tokset = taggerData['tokset']

print('loaded tagger data')

tokCorpus = list()
for i,snt in enumerate(corpus):
    tokCorpus.append([sortedListBinarySearchNoRaise(tokset, wrd) for wrd in snt])
    if i%25000 == 0:
        print('%d of %d'%(i,len(corpus)))

tokCorpus = deepTupleConversion(tokCorpus)

print('loaded corpus - tagging may begin')

dictEmptyTriples = dict(taggerData['keypairs']['3empty'])
dictTriples = dict(taggerData['keypairs']['3middle'])
dictTuplesL = dict(taggerData['keypairs']['2left'])
dictTuplesR = dict(taggerData['keypairs']['2right'])
dictFallback = dict(taggerData['keypairs']['1fallback'])

def getTagFallback(triple):
    return dictFallback.get[triple[1:2]]

def getTagTuplesL(triple):
    return dictTuplesL[triple[0:2]]

def getTagTuplesR(triple):
    return dictTuplesR[triple[1:3]]

def getTagTriples(triple):
    return dictTuplesR[triple[0:3]]

def getTagTriplesEmpty(triple):
    return dictEmptyTriples[triple[0:3:2]]

taggingStrategy = [
        getTagTriples,
        getTagTuplesR,
        getTagTuplesL,
        getTagTriplesEmpty,
        getTagFallback
]

def getTagWithStategy(triple):
    for stategy in taggingStrategy:
        try:
            return stategy(triple)
        except:
            pass
    return -1

def processSentence(tokSentence):
    l = list()
    for i in range(len(tokSentence)):
        triple = (getListItemOr(tokSentence, i-1, None), tokSentence[i], getListItemOr(tokSentence, i+1, None))
        tag = getTagWithStategy(triple)
        l.append((tokSentence[i], tag))
    return l

tokTagged = list()
for i,snt in enumerate(tokCorpus):
    tokTagged.append(processSentence(snt))
    if i%25000 == 0:
        print('%d of %d'%(i,len(tokCorpus)))

print('corpus tagged - preparing for serialization')

taggedCorpus = list()
for words in tokTagged:
    sentence = list()
    for word in words:
        sentence.append(getListItemOr(tagset, word[1], "???"))
    taggedCorpus.append(sentence)

stg = '\n\n'.join(['\n'.join(snt) for snt in taggedCorpus])

print('serialized')

with open('unitexable_test/corpus.txt.tagged.txt','w') as f:
    f.write(stg)

print('done')

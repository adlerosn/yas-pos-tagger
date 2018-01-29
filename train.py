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

from utils import flatten, sortedListBinarySearch, getListItemOr, dictToKeypair

with open('unitexable_train/corpus.txt.answersheet.txt') as f:
    trainSet = [[[wrd.split('/',1)[0].strip().lower(),wrd.split('/',1)[1]] for wrd in snt.strip().splitlines()] for snt in f.read().strip().split('\n\n')]

print('Read from file')

tokSet = tuple(sorted(list(set(map(lambda a: a[0], flatten(trainSet))))))
tagSet = tuple(sorted(list(set(map(lambda a: a[1], flatten(trainSet))))))

print('Int conversion set')

newTrainSet = list()
for i, snt in enumerate(trainSet):
    newTrainSet.append([
            (sortedListBinarySearch(tokSet,wrd[0]),sortedListBinarySearch(tagSet,wrd[1]))
            for wrd in snt
    ])
    if(i%10000 == 0):
        print('%d of %d'%(i,len(trainSet)))

print('Int conversion sentences')

def makeEmptyTriples(lst):
    triples = list()
    for i in range(1,len(lst)-1):
        triples.append(((lst[i-1][0], lst[i+1][0]),lst[i][1]))
    return triples

def makeTriples(lst):
    triples = list()
    for i in range(len(lst)):
        triples.append(((getListItemOr(lst, i-1, [None])[0], lst[i][0], getListItemOr(lst, i+1, [None])[0]),lst[i][1]))
    return triples

def makeTuplesL(lst):
    tuples = list()
    for i in range(1, len(lst)):
        tuples.append(((lst[i-1][0], lst[i][0]),lst[i][1]))
    return tuples

def makeTuplesR(lst):
    tuples = list()
    for i in range(len(lst)-1):
        tuples.append(((lst[i][0], lst[i+1][0]),lst[i][1]))
    return tuples

def makeFallback(lst):
    fallback = list()
    for i in range(len(lst)-1):
        fallback.append(((lst[i][0],),lst[i][1]))
    return fallback

tgfb = tuple(flatten([makeFallback(snt) for snt in newTrainSet]))
tgtl = tuple(flatten([makeTuplesL(snt) for snt in newTrainSet]))
tgtr = tuple(flatten([makeTuplesR(snt) for snt in newTrainSet]))
tgtp = tuple(flatten([makeTriples(snt) for snt in newTrainSet]))
tget = tuple(flatten([makeEmptyTriples(snt) for snt in newTrainSet]))

print('tuples created')

def makeFrequencyTupleDict(tuples):
    d = dict()
    for t in tuples:
        if t[0] not in d:
            d[t[0]] = dict()
        if t[1] not in d[t[0]]:
            d[t[0]][t[1]] = 1
        else:
            d[t[0]][t[1]]+= 1
    return d

def getMostFrequentTupleDict(d1):
    d = dict()
    for tpl,freq in d1.items():
        d[tpl] = sorted([tuple([freq, tag]) for tag,freq in freq.items()])[-1][1]
    return d

kpfb = dictToKeypair(getMostFrequentTupleDict(makeFrequencyTupleDict(tgfb)))
kptl = dictToKeypair(getMostFrequentTupleDict(makeFrequencyTupleDict(tgtl)))
kptr = dictToKeypair(getMostFrequentTupleDict(makeFrequencyTupleDict(tgtr)))
kptp = dictToKeypair(getMostFrequentTupleDict(makeFrequencyTupleDict(tgtp)))
kpet = dictToKeypair(getMostFrequentTupleDict(makeFrequencyTupleDict(tget)))

print('decision keypairs created')

import json

sv = {
      'tagset':tagSet,
      'tokset':tokSet,
      'keypairs': {
              '1fallback': kpfb,
              '2left': kptl,
              '2right': kptr,
              '3middle':kptp,
              '3empty': kpet
      }
}

svt = json.dumps(sv)

print('serialized train data')

with open('unitexable_test/traindata.json','w') as f:
    f.write(svt)

print('saved train data in disk')
print('done')

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

with open('unitexable_test/corpus.answers_final.txt') as f:
    answers = [[word.split('/') for word in sentence.splitlines()] for sentence in f.read().strip().split('\n\n')]

with open('unitexable_test/corpus.guesses_final.txt') as f:
    guesses = [[word.split('/') for word in sentence.splitlines()] for sentence in f.read().strip().split('\n\n')]

assert len(answers) == len(guesses)

tags = list()

for i in range(len(answers)):
    assert len(answers[i]) == len(answers[i])
    for j in range(len(answers[i])):
        assert len(answers[i][j]) == len(answers[i][j])
    tags += list(zip(
            [k[1] for k in answers[i]],
            [k[1] for k in guesses[i]]
    ))

convertAns = [
]

convertGss = [

]

for i, tag in enumerate(tags):
    tag = list(tag)
    for subst in convertAns:
        if tag[0] == subst[0]:
            tag[0] = subst[1]
    for subst in convertGss:
        if tag[1] == subst[0]:
            tag[1] = subst[1]
    tags[i] = tag

allTags = sorted(list(set(flatten(tags))))

confusionMatrix = dict()

equality = {True:0, False:0}

from statisticsMetrics import getConfusionMatrixEmptyData

for tag in allTags:
    confusionMatrix[tag] = getConfusionMatrixEmptyData()

for ans, gss in tags:
    if ans not in confusionMatrix:
        confusionMatrix[ans] = getConfusionMatrixEmptyData()
    if gss not in confusionMatrix:
        confusionMatrix[gss] = getConfusionMatrixEmptyData()
#    if gss == '???':
#        continue
    equality[gss==ans]+=1
    for clazz in allTags:
#        if clazz == '???':
#            continue
        confusionMatrix[clazz][clazz==ans][clazz==gss]+=1
        #        "Preposition" in "True" "Positive" increments

#if '???' in confusionMatrix:
#    del confusionMatrix['???']

import json

with open('unitexable_test/confusion_matrix.json','w') as f:
    f.write(json.dumps(confusionMatrix,indent=4,sort_keys=True))

sumConfusionMatrix = getConfusionMatrixEmptyData()
for cm in confusionMatrix.values():
    for x in [True, False]:
        for y in [True, False]:
            sumConfusionMatrix[x][y] += cm[x][y]

with open('unitexable_test/confusion_matrix_sum.json','w') as f:
    f.write(json.dumps(sumConfusionMatrix,indent=4,sort_keys=True))

with open('unitexable_test/equality.json','w') as f:
    f.write(json.dumps(equality,indent=4,sort_keys=True))

from statisticsMetrics import getStatistics as statistics

with open('unitexable_test/confusion_matrix.stats.json','w') as f:
    f.write(json.dumps({clazz:statistics(cm) for clazz, cm in confusionMatrix.items()},indent=4,sort_keys=True))

with open('unitexable_test/confusion_matrix_sum.stats.json','w') as f:
    f.write(json.dumps(statistics(sumConfusionMatrix),indent=4,sort_keys=True))

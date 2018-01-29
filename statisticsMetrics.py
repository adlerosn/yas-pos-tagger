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

import traceback

def getConfusionMatrixEmptyData():
    '''
    Model
                   | X              | not X          |
    Pred Positive  | True positive  | False positive |
    Pred Negative  | False positive | True negative  |
    '''
    return {
            True:  { True: 0, False: 0 },
            False: { True: 0, False: 0 }
    }

def totalPopulation(cm):
    return cm[True][True]+cm[True][False]+cm[False][True]+cm[False][False]

def predicted(cm, conc):
    return cm[True][conc]+cm[False][conc]

def condition(cm, cond):
    return cm[cond][True]+cm[cond][False]

def readable(cm, s):
    s = s.lower()
    s = s.split(' ')
    if s[0].startswith('t'):
        if s[1].startswith('p'):
            return cm[True][True]
        else:
            return cm[False][False]
    else:
        if s[1].startswith('p'):
            return cm[False][True]
        else:
            return cm[True][False]

def recall(cm):
    try:
        return readable(cm, 't p') / condition(cm, True)
    except:
        return None

def missRate(cm):
    try:
        return readable(cm, 'f n') / condition(cm, True)
    except:
        return None

def specificity(cm):
    try:
        return readable(cm, 't n') / condition(cm, False)
    except:
        return None

def precision(cm):
    try:
        return readable(cm, 't p') / predicted(cm, True)
    except:
        return None

def accuracy(cm):
    try:
        return (readable(cm, 't p') + readable(cm, 't n')) / totalPopulation(cm)
    except:
        return None

def prevalence(cm):
    try:
        return condition(cm, True) / totalPopulation(cm)
    except:
        return None

def f1score(cm):
    try:
        return 2/(1/recall(cm) + 1/precision(cm))
    except:
        return None

def getStatistics(cm):
    return {
            'recall': recall(cm),
            'missRate': missRate(cm),
            'specificity': specificity(cm),
            'precision': precision(cm),
            'accuracy': accuracy(cm),
            'prevalence': prevalence(cm),
            'f1score': f1score(cm),
    }

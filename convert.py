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

import os

encodings_to_try = ['utf-8','iso-8859-1','cp1252','ascii']
dir_to_look_corpora = 'downloaded'

allInOne = []

def decode_try_multiple(stringbytes, encodings = ['utf-8','ascii']):
    lastException = UnicodeDecodeError('empty',b'',0,1,'No encodings provided')
    for encoding in encodings:
        try: return stringbytes.decode(encoding)
        except UnicodeDecodeError as exc: lastException = exc
    raise lastException

for corpus_fn in sorted(list(filter(lambda a: a!='readme.md', os.listdir(dir_to_look_corpora)))):
    corpus_path = os.path.join(dir_to_look_corpora, corpus_fn)
    with open(corpus_path, 'rb') as f:
        fileBytes = f.read()
        fileString = decode_try_multiple(fileBytes, encodings_to_try)
        allInOne.append(fileString.strip())

allInOne = '\n'.join(allInOne).strip()
allInOne = [[word.split('_',1) for word in sentence.split(' ') if len(word)>0] for sentence in allInOne.splitlines()]

x = [[word[0] for word in sentence] for sentence in allInOne]
y = [[word[1] for word in sentence] for sentence in allInOne]

from sklearn.model_selection import train_test_split
train, test = train_test_split(allInOne, test_size=0.6, random_state=96)

tr_s = '\n\n'.join(['\n'.join(['/'.join(wrd) for wrd in snt]) for snt in train])
te_s = '\n\n'.join(['\n'.join(['/'.join(wrd) for wrd in snt]) for snt in test])
te_u = '\n'.join([' '.join([wrd[0] for wrd in snt]) for snt in test])

with open('unitexable_train/corpus.txt.answersheet.txt','w') as f:
    f.write(tr_s)
with open('unitexable_train/corpus.txt','w') as f:
    f.write(tr_s)
with open('unitexable_test/corpus.txt','w') as f:
    f.write(te_s)
with open('unitexable_test/corpus.answersheet.txt','w') as f:
    f.write(te_s)
with open('unitexable_test/corpus.answers_final.txt','w') as f:
    f.write(te_s)
with open('unitexable_test/corpus.txt.untagged.txt','w') as f:
    f.write(te_u)

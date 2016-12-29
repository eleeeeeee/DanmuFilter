#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 22:22:37 2016

@author: root
"""
import gensim as gm
reload(gensim)
workdir = '/home/danmu/'
jb.set_dictionary('/home/toolCodes/dict.txt.big')        
jb.load_userdict(workdir+r'rules/forbid_sex.txt')
texts = []
with open(workdir+r'data/rawData_yanzhi.txt','r') as f:
    for line in f:
        line = line.strip().decode('UTF-8')
        items = jb.cut(line)
        texts.append([i for i in items])
dictionary = gm.corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
print(corpus)
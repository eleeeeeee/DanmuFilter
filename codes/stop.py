#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:15:54 2016

@author: root
"""
STOP_PATH = r'/home/toolCodes/'
def getAllStopSet(kind='All'):
    s = {' ','\n'}
    if (kind=='All') or (kind== 'Chinese'):
        with open(STOP_PATH+'stopwords1_cn.txt') as f:
            for line in f:
                line = line.strip().decode('UTF-8')
                s.add(line)
        with open(STOP_PATH+'stopwords2_cn.txt') as f:
            for line in f:
                line = line.strip().decode('UTF-8')
                s.add(line)
    if (kind=='All') or (kind=='English'):
        with open(STOP_PATH+'stopwords1_en.txt') as f:
            for line in f:
                line = line.strip().decode('UTF-8')
                s.add(line)
    return s
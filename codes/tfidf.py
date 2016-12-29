#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 09:42:48 2016

@author: jeremy
"""
import jieba as jb
workdir = '/home/danmu/'

forbid_set = set()
#   规则列表
with open(workdir+r'rules/forbid_sex.txt','r') as f:
    for line in f.readlines():
        forbid_set.add(line.strip().decode('UTF-8'))

jb.set_dictionary('/home/toolCodes/dict.txt.big')        
#jb.load_userdict(workdir+r'rules/forbid_sex.txt')
#   过滤文本 -- by token
corpus = []
normal = open(workdir+r'data/yanzhi_bad.txt','w')
with open(workdir+r'data/rawData_yanzhi.txt','r') as f:
    for line in f:
        line = line.strip().decode('UTF-8')
        items = jb.cut(line)
        print('|'.join(items))
        flag=0
        for item in items:
            if item in forbid_set:
                corpus.append(line)
                print(line)
                normal.write(line.encode('UTF-8')+'\n')
                flag=1
                break
        if flag == 0:
            print(line)

normal.close()
######################################
#         统计所有词频（分别对词、单字）
######################################
import jieba.analyse
import stop
jieba.set_dictionary('/home/toolCodes/dict.txt.big')
jb.load_userdict(workdir+r'rules/forbid_sex.txt')
stop_set = stop.getAllStopSet()
LEN = 20000  #样本容量
TOPK = 50  #取前K个热词
tfDictByOne = {}
tfDictByMulti = {}
with open(workdir+'data/rawData_yanzhi.txt') as f:
    for line in f.readlines()[:LEN]:
        line = line.decode('UTF-8').strip()
        items = jb.cut(line)
        for i in items:
            if i not in stop_set:
                tfDictByMulti[i] = tfDictByMulti.get(i,0)+1
        for i in line:
            if i not in stop_set:       #拆成单字
                tfDictByOne[i] = tfDictByOne.get(i,0)+1

sortedListByOne = sorted(tfDictByOne.iteritems(),key=lambda x:x[1],reverse=True)
sortedListByMulti = sorted(tfDictByMulti.iteritems(),key=lambda x:x[1],reverse=True)
for item in sortedListByMulti[:TOPK]:
    print(item[0])
    print(item[1])
    
content = open(workdir+'data/rawData_yanzhi.txt').read()
tags = jieba.analyse.extract_tags(content, topK=TOPK)
for i in tags:
    print(i)
    
    

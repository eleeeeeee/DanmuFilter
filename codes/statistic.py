#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 09:56:44 2016

@author: root
"""

import pandas as pd
import jieba.analyse
import jieba as jb
import re
import stop
workdir = '/home/danmu/'
#词性
POS ={	
		"a":"形容词","ad":"副形词","an":"名形词","ag":"形容词性语素","b":"区别词",
      	"c":"连词","d":"副词","df":"副词","dg":"副词","e":"叹词","f":"方位词",
      "g":"语素","j":"略语","i":"成语","h":"前缀","l":"习用语","k":"后缀",
      "m":"数词","mg":"数词","mq":"数量词","n":"名词","nr":"人名","ng": "名词性语素",
		"nrfg":"人名","nrt":"人名","ns":"地名","nt":"机构团体名","nz":"其它专名",
      "r":"代词","q":"量词","p":"介词","o":"拟声词","r": "代词", "rr":"人称代词",
		"rz":"指示代词","rg":"代词性语素","u":"助词","t":"时间词",
      "s":"处所词","tg":"时间词性语素","ud":"助词","ug":"助词","uj":"助词",
		"ul":"助词","uv":"助词","uz":"助词","v":"动词","vd":"副动词",
		"vn":"名动词","vq":"动词","vi":"不及物动词（内动词）","vg":"动词性语素",
       "x":"字符串","xu":"网址URL","xx":"非语素字","xu":"网址URL","y":"语气词",
       "yg":"语气词","z":"状态词"
}



#获取关键词的概率分布 top50 lines20000
def getKeyWords(fileName,top = 50,lines = 20000):
    jieba.set_dictionary('/home/toolCodes/dict.txt.big')
    jb.load_userdict(workdir+r'rules/forbid_sex.txt')
    stop_set = stop.getAllStopSet()     #加载停用词表
    tfDictByOne = {};tfDictByMulti = {} #单字、单词
    with open(fileName) as f:
        for line in f.readlines()[:lines]:
            line = line.decode('UTF-8').strip()
            items = jb.cut(line,HMM=False)
            #print('|'.join(items))
            for i in items:
                if i not in stop_set:       #拆成词组
                    tfDictByMulti[i] = tfDictByMulti.get(i,0)+1
            for i in line:
                if i not in stop_set:       #拆成单字
                    tfDictByOne[i] = tfDictByOne.get(i,0)+1
    
    for k in tfDictByOne.keys():
        tfDictByOne[k]/=(lines*1.0)
    for k in tfDictByMulti.keys():
        tfDictByMulti[k]/=(lines*1.0)
    sortedListByOne = sorted(tfDictByOne.iteritems(),key=lambda x:x[1],reverse=True)
    sortedListByMulti = sorted(tfDictByMulti.iteritems(),key=lambda x:x[1],reverse=True)
    for item in sortedListByOne[:top]:
        print(item[0])
        print(item[1])
    return sortedListByOne,sortedListByMulti
    
sortedListByOne,sortedListByMulti = getKeyWords(workdir+r'data/rawData_yanzhi.txt',50)
with open('/home/xls/singleKeywordDistribution_xls.txt','w') as f:
     for i in sortedListByOne[:50]:
            f.write(i[0].encode('UTF-8'))
            f.write(','+str(i[1])+'\n')
'''    
pageRank -->关键词
content = open(workdir+r'data/rawData_yanzhi.txt').read()
tags = jieba.analyse.textrank(content, topK=200,withWeight=True)
for i in tags:
    print(i[0])
    print(i[1])
'''    
    
#----------------------------------------

#弹幕文本长度的概率分布情况,并导出到文本中
def getLengthDistribution(filename):
    lenDict = {};num = 0
    with open(filename,'r') as f:
        for line in f.readlines():
            num+=1
            line = line.strip().decode('UTF-8')
            items = line.split(',')
            l = len(','.join(items[5:]))
            lenDict[l] = lenDict.get(l,0)+1
    for k in lenDict.keys():
        lenDict[k]/=(num*1.0)
    sortedList =  sorted(lenDict.iteritems(),key=lambda x:x[0])
    with open('/home/xls/lenDistribution_xls.txt','w') as f:
        for i in range(len(sortedList)):
            f.write(str(sortedList[i][0])+','+str(sortedList[i][1])+'\n')
    return sortedList

def getLengthAbnormalDistribution(filename,sep=','):
    lenDict = {};num = 0
    with open(filename,'r') as f:
        for line in f:
            num+=1
            line = line.strip().decode('UTF-8')
            items = line.split(sep)
            l = len(','.join(items[:-1]))
            d = lenDict.get(l,[0,0])
            if (items[-1]=='1'):
                d[1]+=1
            else:
                d[0]+=1
            lenDict[l] = d
    for k in lenDict.keys():
        lenDict[k][0]/=(num*1.0)
        lenDict[k][1]/=(num*1.0)
    sortedList =  sorted(lenDict.iteritems(),key=lambda x:x[0])
    with open('/home/xls/lenAbnorDistribution_xls.txt','w') as f:
        for i in range(len(sortedList)):
            f.write(str(sortedList[i][0])+','+str(sortedList[i][1][0])+','+str(sortedList[i][1][1])+'\n')
    return sortedList
    
lenList = getLengthDistribution('/home/smp2016/valid_status.txt')

#----------------------------------------    

#获取词性概率分布 top50 lines20000
def getTermKindDistribution(fileName):
    jb.enable_parallel(8)
    termMap = {};num = 0
    with open(fileName) as f:
        for line in f:
            num+=1
            line = line.strip().decode('UTF-8')
            words = jb.posseg.cut(line)
            for word, flag in words:
                termMap[flag] = termMap.get(flag,0)+1
#                print(word)
#                print(flag)
    for k in termMap.keys():
        if POS.has_key(k):
            termMap[POS[k]] = termMap[k]/(1.0*num)
        elif POS.has_key(k[0]):
            termMap[POS[k[0]]] = (termMap.get(POS[k[0]],0)+termMap[k])/(1.0*num)
        del termMap[k]
    termlist = sorted(termMap.iteritems(),key=lambda x:x[1],reverse=True)
    return termlist
    
termlist =  getTermKindDistribution(workdir+r'data/rawData_youxi2.txt')
with open('/home/xls/termKindDistribution_xls.txt','w') as f:
    for i in termlist:
        f.write(i[0])
        f.write(','+str(i[1])+'\n')






TOPK = 500  #取前K个热词
jb.load_userdict(workdir+r'rules/forbid_sex.txt')
danmu = pd.read_csv(workdir+'data/notedData_yanzhi.csv',names = ['danmu','label'],encoding='utf-8')
content = open(workdir+'data/rawData_yanzhi.txt').read().decode('UTF-8')
tags = jieba.analyse.extract_tags(content, topK=TOPK)
hot_term = [];hot_term_0 = dict();hot_term_1 = dict()
pattern = re.compile(r'[0-9\.]+') 
for i in tags:
    match = pattern.match(i)
    if not match:
        hot_term.append(i) 
for i in hot_term:
    if i=='++':
        i = '\+\+'
    pattern = re.compile(i)
    for j in range(danmu.shape[0]):
        if pattern.match(danmu['danmu'][j]):
            if danmu['label'][j]==1:
                hot_term_1[i] = hot_term_1.get(i,0)+1
            else :
                hot_term_0[i] = hot_term_0.get(i,0)+1
        
sortedListByOne = sorted(hot_term_1.iteritems(),key=lambda x:x[1],reverse=True)
sortedListByZero = sorted(hot_term_0.iteritems(),key=lambda x:x[1],reverse=True)    
listOne = [];listZero = [];listTerm = []
for i in sortedListByOne[:50]:
    listOne.append(i[1]/(danmu.shape[0]*1.0))
    listZero.append(hot_term_0.get(i[0],0)/(danmu.shape[0]*1.0))
    listTerm.append(i[0])

xls = open(workdir+'data/xls.txt','w')
for i in range(len(listTerm)):
    xls.write(listTerm[i].encode('UTF-8'))
    xls.write(','+str(listZero[i])+','+str(listOne[i])+'\n')
xls.close()    
    

import numpy as np
from matplotlib import pyplot as plt
from pylab import mpl  
plt.figure(figsize=(16,8))
n = len(listTerm)
X = np.arange(n)*5
#X是1,2,3,4,5,6,7,8,柱的个数
# numpy.random.uniform(low=0.0, high=1.0, size=None), normal
#uniform均匀分布的随机数，normal是正态分布的随机数，0.5-1均匀分布的数，一共有n个
Y1 = np.array(listOne)
Y2 = np.array(listZero)
plt.bar(X,Y1,width=2.5,facecolor = 'lightskyblue',edgecolor = 'white')
#width:柱的宽度
plt.bar(X+2.5,Y2,width=2.5,facecolor = 'yellowgreen',edgecolor = 'white')
plt.legend(['abnormal','normal'],loc='upper right',fontsize=24)
plt.ylim(0,0.1)
plt.title('yanzhi', fontsize=24)
plt.xlabel('Top 50 key words', fontsize=20)
plt.ylabel('term frequence', fontsize=20)
plt.show()
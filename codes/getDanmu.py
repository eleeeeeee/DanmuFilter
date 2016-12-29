#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 16:45:23 2016

@author: root
"""
import time, sys

from danmu import DanMuClient
def pp(msg):
    print(msg)
#    print(msg.encode(sys.stdin.encoding, 'ignore').
#        decode(sys.stdin.encoding))

dmc = DanMuClient('http://www.panda.tv/27337')
if not dmc.isValid(): print('Url not valid')

@dmc.danmu
def danmu_fn(msg):
    pp('[%s] %s' % (msg['NickName'], msg['Content']))
    print(msg)
@dmc.gift
def gift_fn(msg):
    pp('[%s] sent a gift!' % msg['nn'])

@dmc.other
def other_fn(msg):
    pp('Other message received')
dmc.start(blockThread = True)

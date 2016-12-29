import time, sys

import danmu as dm
reload(dm)
def pp(msg):
    i=0

dmc = dm.DanMuClient('http://www.panda.tv/11299')
if not dmc.isValid(): print('Url not valid')

@dmc.danmu
def danmu_fn(msg):
    pp('[%s] %s' % (msg['NickName'], msg['Content']))

@dmc.gift
def gift_fn(msg):
    pp('[%s] sent a gift!' % msg['NickName'])

@dmc.other
def other_fn(msg):
    pp('Other message received')

dmc.start(blockThread=True)
#dmc.stop()
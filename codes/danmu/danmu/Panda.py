#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import time, sys, re, json,os
import socket, select
from struct import pack
import csv
import requests
from .Abstract import AbstractDanMuClient

class _socket(socket.socket):
    def communicate(self, data):
        self.push(data)
        return self.pull()
    def push(self, data):
        self.sendall(data)
    def pull(self):
        try: # for socket.settimeout
            return self.recv(9999)
        except:
            return ''

class PandaDanMuClient(AbstractDanMuClient):
    curnum=0    #弹幕条数
    isload = False #房间信息是否被加载
    #获取主播信息和房间信息
    def _extract_roominfo(self,j,strTag = '\"'):
        path = self.__workdir__+'data/pandas/roominfo'
        if not os.path.isdir(path):os.makedirs(path)
        j_hostinfo = j.get('hostinfo',{})
        j_roominfo = j.get('roominfo',{})
        room_id = j_roominfo.get('id','')  #roomid
        start_time = j_roominfo.get('start_time','') #start_time
        self.liveid = room_id+'_'+start_time #liveid
        self.person_num = j_roominfo.get('person_num','')
        end_time = j_roominfo.get('end_time','')  #end_time
        host_id = j_hostinfo.get('rid',-1)
        self.cate = j_roominfo.get('cate','')
        fans = j_roominfo.get('fans','')
        weight = j_hostinfo.get('bamboos','')
        avater = j_roominfo.get('pictures',{}).get('img','')
        filename = path+'/'+self.cate+'.csv'
        val = [self.liveid,start_time,end_time,room_id,host_id,self.cate,fans,weight,avater]
        if not PandaDanMuClient.isload:
            isExist,self.hislivid = self.loadhistoryliveid(filename)
            PandaDanMuClient.isload = True
        if self.liveid not in self.hislivid:
            (self.hislivid).add(self.liveid)
            with open(filename, 'ab') as f:
                writer = csv.writer(f,quotechar=strTag)
                writer.writerow(val)
    def _get_live_status(self):
        params = {
            'roomid': (self.url.split('/')[-1] or
                self.url.split('/')[-2]),
            'pub_key': '',
            '_': int(time.time()), }
        j = requests.get('http://www.panda.tv/api_room', params).json()['data']
        #获取房间信息
        #self._extract_roominfo(j)
        return j['videoinfo']['status'] == '2'
    def _prepare_env(self):
        roomId = self.url.split('/')[-1] or self.url.split('/')[-2]
        url = 'http://www.panda.tv/ajax_chatroom?roomid=%s&_=%s'%(roomId, str(int(time.time())))
        roomInfo = requests.get(url).json()
        url = 'http://api.homer.panda.tv/chatroom/getinfo'
        params = {
            'rid': roomInfo['data']['rid'],
            'roomid': roomId,
            'retry': 0,
            'sign': roomInfo['data']['sign'], 
            'ts': roomInfo['data']['ts'],
            '_': int(time.time()), }
        serverInfo = requests.get(url, params).json()['data']
        serverAddress = serverInfo['chat_addr_list'][0].split(':')
        return (serverAddress[0], int(serverAddress[1])), serverInfo
    def _init_socket(self, danmu, roomInfo):
        data = [
            ('u', '%s@%s'%(roomInfo['rid'], roomInfo['appid'])),
            ('k', 1),
            ('t', 300),
            ('ts', roomInfo['ts']),
            ('sign', roomInfo['sign']),
            ('authtype', roomInfo['authType']) ]
        data = '\n'.join('%s:%s'%(k, v) for k, v in data)
        data = (b'\x00\x06\x00\x02\x00' + pack('B', len(data)) +
            data.encode('utf8') + b'\x00\x06\x00\x00')
        self.danmuSocket = _socket(socket.AF_INET, socket.SOCK_STREAM)
        self.danmuSocket.settimeout(3)
        self.danmuSocket.connect(danmu)
        self.danmuSocket.push(data)
    def _create_thread_fn(self, roomInfo):
        def get_danmu(self):
            if not select.select([self.danmuSocket], [], [], 1)[0]: return
            content = self.danmuSocket.pull()
            for msg in re.findall(b'({"type":.*?}$)', content):
                try:
                    msg = json.loads(msg.decode('UTF-8', 'ignore'))
                    #获取弹幕信息
                    self.msg_type = msg.get('type','')
                    if self.msg_type=='1':      #弹幕
                        #self._extract_danmu(msg)
                        PandaDanMuClient.curnum+=1
                    elif self.msg_type=='306':  # 雪花/姜饼
                        self.content = msg.get('data',{}).get('content','').get('price','')
                        print(msg)
                    elif (self.msg_type=='207') or (self.msg_type=='208'): #访客信息
                        pass
                    else:
                        print(msg)
                    msg['MsgType'] = ''
                except:
                    pass
                else:
                    self.danmuWaitTime = time.time() + self.maxNoDanMuWait
                    self.msgPipe.append(msg)
        def heart_beat(self):
            self.danmuSocket.push(b'\x00\x06\x00\x06')
            self._get_live_status()
            time.sleep(60)
        return get_danmu, heart_beat
    # 弹幕提取
    def _extract_danmu(self,msg,strTag = '\"'):
            path = self.__workdir__+'data/pandas/danmuinfo'
            print(path+'/'+self.cate+'.csv')
            if not os.path.isdir(path):os.makedirs(path)
            cur_time = msg.get('time',-1)
            msgfrom = msg.get('data', {}).get('from', {})
            user_id = msgfrom.get('rid','')
            level = msgfrom.get('level','') 
            nickname = msgfrom.get('nickName','').encode('UTF-8')
            plat = msgfrom.get('__plat','')
            content = msg.get('data',{}).get('content','').encode('UTF-8')
            val = [self.liveid,cur_time,self.person_num,user_id,level,plat,nickname,content]
            with open(path+'/'+self.cate+'.csv', 'ab') as f:
                writer = csv.writer(f,quotechar=strTag)
                writer.writerow(val)
                
                
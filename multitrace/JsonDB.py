#!/opt/exptools/bin/python
__author__ = 'sanpingz'

from os.path import join, abspath
import os, time
import pickle
import SimpleFTP


BASE_DIR = abspath('data')
LOCAL = 'pcap'

class simpleDB:
    user = {}
    def __init__(self, username):
        self.username = username
        self.userfile = join(BASE_DIR, str(username)+'.json')
    def confirm(self):pass
    def isExist(self):
        return os.path.isfile(self.userfile)
    def load(self):
        old = {}
        if self.isExist():
            file = open(self.userfile, 'rb')
            try:
                old = pickle.load(file)
            except EOFError, IOError:
                old = {}
            file.close()
        return old
    def add(self, user):
        old = self.load()
        old.update(user)
        file = open(self.userfile, 'wb')
        if self.isExist():
            try:
                pickle.dump(old, file)
            finally: file.close()
        else:
            try:
                pickle.dump(old, file)
            finally:
                file.close()
                command = 'chmod 755 '+self.userfile
                os.system(command)
    def save(self, data):
        file = open(self.userfile, 'wb')
        try:
            pickle.dump(data, file)
        finally: file.close()
    def remove(self, ctid):
        old = self.load()
        file = open(self.userfile, 'wb')
        try:
            del old[ctid]
            pickle.dump(old, file)
        finally: file.close()
    def select(self, ctid):
        old = self.load()
        if old.has_key(ctid):
            return old[ctid]
        else:
            return {}
    def update(self, user):
        self.add(user)
    def filter(self, expires=7200):
        old = dict(self.load())
        data = {}
        if old:
            for key, value in old.items():
                alt = int(time.time()-value['time'])
                exp = int(value['duration'])*60
                if alt <= expires:
                    if alt >= exp and value['status'] == 'Started':
                        param = SimpleFTP.parameter
                        param['labip'] = value['labip']
                        param['ctid'] = value['ctid']
                        param['local'] = LOCAL
                        addr = SimpleFTP.addr(param=param, duration=24)
                        if addr and (len(addr)>0) and (len(addr)<120):
                            value['status'] = 'Stopped'
                            value['addr'] = addr
                        else:
                            value['status'] = 'Failure'
                            data[key] = value
                    data[key] = value
        self.save(data)
        return data

if __name__ == '__main__':
    sd = simpleDB('sanpingz')
    TIMEFORMAT = '%Y-%m-%d %X'
    cnt = time.time()+time.altzone+8*3600
    startime = time.strftime(TIMEFORMAT, time.localtime(cnt))
    user = {
        '1':{'ctid':1,
             'mode':'SIPURI',
             'callid':'sip:+16310001@ln010.lucentlab.com',
             'duration':1,
             'labip':'135.2.121.97',
             'status':'Started',
             'startime':startime,
             'time': time.time()
        }
    }
    sd.add(user)
    #sd.save(user)
    #sd.remove('2')
    #sd.update(user)
    #print sd.select('3')
    print sd.load()
    #print sd.filter()

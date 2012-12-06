#!/opt/exptools/bin/python
__author__ = 'sanpingz'

from os.path import join, abspath
import os, time
import shelve
from FTPDownload import ftpDownload
import FTPDownload

BASE_DIR = abspath('data')
dbpath = join(BASE_DIR, 'tracedb')
class simpleDB:
    user = {}
    def __init__(self, key):
        self.db = shelve.open(dbpath)
        self.key = key
    def confirm(self):pass
    def isExist(self):
        return self.db.has_key(self.key)
    def load(self):
        return self.db.get(self.key)
    def add(self, item):
        user = {}
        items = {}
        if self.isExist():
            items = self.load()
        items[str(item['ctid'])] = item
        self.update(items)
    def save(self, user):
        self.db[self.key] = user
    def remove(self, ctid):
        if self.db.has_key(self.key):
            del self.db[self.key]
    def select(self, ctid):
        item = {}
        if self.db.has_key(self.key):
            item = self.db.get(self.key).get(ctid)
        return item
    def update(self, items):
        user = self.load()
        if not user:
            user = {}
        user.update(items)
        self.db[self.key] = user
    def flush(self):
        self.db.sync()
    def close(self):
        self.db.close()
    def filter(self, expires=7200):
        old = self.load()
        data = {}
        if old:
            for key, value in old.items():
                alt = int(time.time()-value['time'])
                exp = int(value['duration'])*60
                if alt <= expires:
                    if alt >= exp and value['status'] == 'Started':
                        param = FTPDownload.parameter
                        param['host'] = value['labip']
                        param['ctid'] = value['ctid']
                        fd = ftpDownload(param)
                        addr = fd.getAddr()
                        if addr and (len(addr)>0) and (len(addr)<128):
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
    item = {'ctid':2,
            'mode':'SIPURI',
            'callid':'sip:+16310001@ln010.lucentlab.com',
            'duration':10,
            'labip':'135.2.121.97',
            'status':'Started',
            'startime':startime,
            'time': time.time()
    }
    items = {'1':{'ctid':1,
                 'mode':'SIPURI',
                 'callid':'sip:+16310001@ln010.lucentlab.com',
                 'duration':30,
                 'labip':'135.2.121.97',
                 'status':'Started',
                 'startime':startime,
                 'time': time.time()}
    }
    #sd.add(item)
    sd.save(items)
    #sd.remove('2')
    #sd.update(items)
    #print sd.select('2')
    #sd.flush()
    print sd.load()
    #print sd.filter()
    sd.close()

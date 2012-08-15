__author__ = 'sanpingz'

from os.path import join, abspath
import sys, os
import pickle

BASE_DIR = abspath('data')

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
                try:
                    old = pickle.load(file)
                except EOFError, IOError:
                    old = {}
            finally: file.close()
        return old
    def save(self, user):
        old = self.load()
        old.update(user)
        file = open(self.userfile, 'wb')
        try:
            pickle.dump(old, file)
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
        self.save(user)

if __name__ == '__main__':
    sd = simpleDB('sanpingz')
    user = {
        '2':{'ctid':'2',
             'mode':'SIPURI',
             'callid':'sip:+16310001@ln010.lucentlab.com',
             'duration':'60',
             'labip':'135.2.121.97',
             'status':'OK',
             'starttime':'2012-8-12'
        }
    }
    #sd.save(user)
    sd.remove('2')
    #sd.update(user)
    #print sd.select('3')
    print sd.load()

#!/opt/exptools/bin/python
__author__ = 'sanpingz'

import re, socket, os
from ftplib import FTP
from os.path import join

parameter = {'host':'135.252.226.34',
         'user':'lss',
         'passwd':'lss',
         'cwd':'../../../logs/ctlog',
         'path':'/logs/ctlog'
}
class sFTP:
    def __init__(self,param):
        self.host = param['host']
        self.user = param['user']
        self.passwd = param['passwd']
        self.cwd = param['cwd']
        self.path = param.get('path')
    def login(self):
        self.ftp = FTP(self.host)
        self.ftp.login(self.user, self.passwd)
        self.ftp.cwd(self.path)
    def close(self):
        self.ftp.quit()
        self.ftp.close()
    def listFiles(self):
        lt = []
        try:
            self.ftp.set_pasv(0)
            try:
                lt = self.ftp.nlst()
            except socket.error:
                #print "port"
                self.ftp.set_pasv(1)
                lt = self.ftp.nlst()
        except: pass
        return lt
    def matchFile(self, fList, ctid):
        matched = ''
        maxValue = 0
        reg = str(ctid)+'[\.|\,]\d{8}\.\d{4}[\.|\,]ISC\.\w+$'
        pattern = re.compile(reg)
        if fList:
            for file in fList:
                if pattern.match(file) and int(re.split('[,|.]+',file)[2])>=maxValue:
                    matched = file
                    maxValue = int(re.split('[,|.]+',file)[2])
        return  matched
    def getAddr(self, flag='ftp', fList=[], ctid=0):
        """flag = ftp|scp|file"""
        file = self.matchFile(fList=fList, ctid=ctid)
        addr = ''
        if file:
            if flag == 'ftp':
                addr = r'ftp://'+self.user+':'+self.passwd+'@'+self.host+r'/'+self.cwd+r'/'+file
            if flag == 'scp':
                addr = self.user+r'@'+self.host+r':'+self.path+r'/'+file
            if flag == 'file':
                addr = self.path+r'/'+file
        return addr
    def mget(self,fns, dst='pcap'):
        if not os.path.isdir(dst):
            os.mkdir(dst)
        buf_size = 1024
        fList = []
        for file in fns:
            fn = join(dst,os.path.split(file)[-1])
            with open(fn, 'wb') as f:
                self.ftp.retrbinary('RETR '+file, f.write, buf_size)
            fList.append(fn)
        return fList

def download(*ids):
    fd = sFTP(parameter)
    fd.login()
    fns = []
    fList = fd.listFiles()
    try:
        for ctid in ids:
            fn = fd.getAddr(flag='file',fList=fList, ctid=ctid)
            if fn:
                fns.append(fn)
        fns = fd.mget(fns)
    except Exception, e:
        print e
        fd.close()
    return fns


if __name__ == '__main__':
    #fd = sFTP(parameter)
    #fd.login()
    #fList = fd.listFiles()
    #print fList
    #print fd.matchFile(fList,15)
    #print fd.getAddr(flag='file',fList=fList,ctid=15)
    #fd.close()

    print download(11,12,13,14)
__author__ = 'sanpingz'

from ftplib import FTP
import os, re, sys

class sFTP(FTP):
    def __init__(self, *arg, **args):
        FTP.__init__(self, *arg, **args)
        self.set_pasv(False)
    def get(self, dn=''):
        print 'Transfer start'
        ls = []
        buf_size = 1024
        if isinstance(dn, list):
            ls = dn
        else:
            ls = self.nlst(dn)
        for file in ls:
            f = open(file, 'wb')
            self.retrbinary('RETR '+file, f.write, buf_size)
            f.close()
            print file+' 200 OK'
        print 'Transfer successfully'
    def put(self, dn=''):
        print 'Transfer start'
        ls = []
        buf_size = 1024
        if isinstance(dn, list):
            ls = dn
        else:
            ls = os.listdir(dn)
        for file in ls:
            f = open(file, 'rb')
            self.storbinary('STOR '+file, f.read, buf_size)
            f.close()
            print file+' 200 OK'
        print 'Transfer successfully'
    def rmdir(self, dn):
        pwd = self.pwd()
        self.cwd(dn)
        for file in  self.nlst():
            self.delete(file)
        for dir in self.dir():
            if self.dir(dir) or self.nlst(dir):
                self.rmdir(dir)
            else: self.rmd(dir)
        self.cwd('..')
        self.rmd(pwd)
        print 'Deleted '+ dn
    def sdir(self, *args):
        lt = []
        st = self.dir(*args)
        ls = st.split('\n')
        for line in ls:
            s = re.findall(r'\w+$', line)
            if s: lt.append(s[0])
        return lt
    def isdir(self, dn):
        flag = False
        f = open('out', 'a')
        out = sys.stdout
        self.dir()
        sys.stdout = out
        ls = out.read().split('\n')
        for line in ls:
            if re.findall(dn, line) and line.startswith('d'):
                flag = True
                break
        return flag


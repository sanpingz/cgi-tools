__author__ = 'sanpingz'

from ftplib import FTP
import os, re, sys

class sFTP(FTP):
    def __init__(self, *arg, **args):
        FTP.__init__(self, *arg, **args)
        self.set_pasv(False)
    def get(self, fn='', mode='wb'):
        buf_size = 1024
        with open(os.path.split(fn)[1], mode) as f:
            self.retrbinary('RETR '+fn, f.write, buf_size)
        print '%-20s 200 OK' % os.path.split(fn)[1]
    def mget(self, dn=''):
        print 'Transfer start'
        print '='*25
        ls = []
        buf_size = 1024
        if isinstance(dn, list):
            ls = dn
        else:
            ls = self.nlst(dn)
            print ls
        for file in ls:
            with open(os.path.split(file)[1], 'wb') as f:
                self.retrbinary('RETR '+file, f.write, buf_size)
            print '%-20s 200 OK' % file
        print '='*25
        print 'Transfer successfully'
    def put(self, fn='', mode='rb'):
        buf_size = 1024
        with open(fn, mode) as f:
            self.storbinary('STOR '+os.path.split(fn)[1], f, buf_size)
        print '%-20s 200 OK' % os.path.split(fn)[1]
    def mput(self, dn=''):
        print 'Transfer start'
        print '='*25
        ls = []
        buf_size = 1024
        if isinstance(dn, list):
            ls = dn
        else:
            ls = map(lambda f: os.path.join(dn,f), os.listdir(dn))
        for file in ls:
            with open(file, 'rb') as f:
                self.storbinary('STOR '+os.path.split(file)[1], f, buf_size)
            print '%-20s 200 OK' % os.path.split(file)[1]
        print '='*25
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
    def isdir(self, dn):
        flag = False
        f = open('out', 'a')
        bak = sys.stdout
        sys.stdout = f
        self.dir()
        f.close()
        sys.stdout = bak
        with open('out') as f:
            ls = f.read().split('\n')
        for line in ls:
            if re.findall(dn, line) and line.startswith('d'):
                flag = True
                break
        return flag


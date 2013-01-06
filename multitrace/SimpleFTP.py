#!/opt/exptools/bin/python
__author__ = 'sanpingz'

import re, socket, os, time
from ftplib import FTP
from os.path import join
from mergePCAP import mergePCAP, genName

parameter = {'host':'135.252.226.34',
         'user':'lss',
         'passwd':'lss',
         'cwd':'../../../logs/ctlog',
         'path':'/logs/ctlog',
         'local':'pcap'
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
        """flag = ftp|scp|remote|local"""
        file = self.matchFile(fList=fList, ctid=ctid)
        addr = ''
        if file:
            if flag == 'ftp':
                addr = r'ftp://'+self.user+':'+self.passwd+'@'+self.host+r'/'+self.cwd+r'/'+file
            if flag == 'scp':
                addr = self.user+r'@'+self.host+r':'+self.path+r'/'+file
            if flag == 'remote':
                addr = self.path+r'/'+file
            if flag == 'local':
                addr = join(parameter['local'],file)
        return addr
    def mget(self,fns):
        #if not os.path.isdir(dst):
        #    os.mkdir(dst)
        dst = parameter['local']
        buf_size = 1024
        fList = []
        for file in fns:
            fn = join(dst,os.path.split(file)[-1])
            f = open(fn, 'wb')
            try:
                self.ftp.retrbinary('RETR '+file, f.write, buf_size)
            finally: f.close()
            #with open(fn, 'wb') as f:
            #    self.ftp.retrbinary('RETR '+file, f.write, buf_size)
            fList.append(fn)
        return fList

def download(ids,param=parameter):
    fd = sFTP(param)
    fd.login()
    fns = []
    fList = fd.listFiles()
    dst = param['local']
    if not os.path.isdir(dst):
        os.mkdir(dst)
    try:
        for ctid in ids:
            fn = fd.getAddr(flag='remote',fList=fList, ctid=ctid)
            if fn and os.path.split(fn)[-1] not in os.listdir(dst):
                fns.append(fn)
        fns = fd.mget(fns)
    except Exception, e:
        #print e
        fd.close()
    return fns

def getLatest(fList,ctid,dst=parameter['local']):
    matched = ''
    maxValue = 0.0
    reg = str(ctid)+'[\.|\,]\d{8}\.(\d{6}|\d{4})[\.|\,]\w+'
    pattern = re.compile(reg)
    if fList:
        for file in fList:
            cTime = os.stat(join(dst,file)).st_ctime
            if pattern.match(file) and cTime>=maxValue:
                matched = file
                maxValue = cTime
    return matched

def addr(ctid, param=parameter, duration=0):
    dst = param['local']
    matched = ''
    try:
        if not os.path.isdir(dst):
            os.mkdir(dst)
        if not isinstance(ctid, list):
            matched = getLatest(os.listdir(dst),ctid,dst=dst)
        if not matched and str(ctid).isdigit():
            fns = download([ctid], param=param)
            if fns:
                for i in range(len(fns)):
                    fns[i] = os.path.split(fns[i])[-1]
                matched = getLatest(fns,ctid)
        if not matched and isinstance(ctid,list):
            ctid = map(int,ctid)
            ctid.sort()
            ctid_str = ''
            for ii in ctid:
                ctid_str += str(ii)+'.'
            ctid_str = ctid_str[:-1]
            matched = getLatest(os.listdir(dst),ctid_str,dst=dst)
            if not matched:
                ftp = sFTP(param)
                fns = []
                for item in ctid:
                    fns.append(ftp.getAddr(flag='local',fList=os.listdir(param['local']),ctid=item))
                matched = mergePCAP(fns,name=join(param['local'],genName(fns)))
                if matched:
                    matched = os.path.split(matched)[-1]
        if matched:
            matched = join(dst,matched)
    except:
        matched = ''
    if duration:
        try:
            """duration = 24h"""
            mergePCAP.rmPCAP(duration=duration,dir=param['local'])
        except:pass
    return  matched


if __name__ == '__main__':
    #fd = sFTP(parameter)
    #fd.login()
    #fList = fd.listFiles()
    #print fList
    #print fd.matchFile(fList,15)
    #print fd.getAddr(flag='local',fList=fList,ctid=16)
    #fd.close()

    #print getLatest(os.listdir('pcap'),17)
    print addr([16,18,19])

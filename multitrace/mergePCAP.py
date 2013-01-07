#!/usr/bin/env python
"""Usage: mergePCAP(.py) PCAP_FILE ...
Tips: Return 0 means failed, return merged file name means successful
"""
__author__ = 'sanpingz'

import os, struct, time, re, sys
from os.path import join
from logCtrl import simpleLog
from pprint import pprint

LOG_FILE = join('data', 'calltrace.log')

def logException():
    simpleLog(name='mergepcap', file=LOG_FILE)

class PCAP:
    headerLen = 24
    capHeaderLen = 16
    magicLen = 4
    #IpHeaderLen=20, UdpHeaderLen=8
    sipGenHeaderLen = 28
    capStructure = ['gmtTime','microTime','capLen','len']
    def __init__(self, fn):
        self.file = open(fn, 'rb')
        #self.file.seek(self.headerLen,0)
        self.previous = 0
        self.current = self.headerLen
    def isPCAP(self):
        now = self.file.tell()
        self.file.seek(0,0)
        magic = self.file.read(self.magicLen)
        self.file.seek(now,0)
        #'0xd4c3b2a1' '\xd4\xc3\xb2\xa1'
        #'0xa1b2c3d4' '\xa1\xb2\xc3\xd4'
        return magic == '\xd4\xc3\xb2\xa1' or magic == '\xa1\xb2\xc3\xd4'
    def header(self):
        now = self.file.tell()
        self.file.seek(0,0)
        header = self.file.read(self.headerLen)
        self.file.seek(now)
        return header
    def sip(self,size,offset):
        now = self.file.tell()
        self.file.seek(offset+self.sipGenHeaderLen+self.capHeaderLen,0)
        msg = self.file.read(size-self.sipGenHeaderLen)
        self.file.seek(now)
        return msg
    def capHeader(self):
        #print 'tell: (before)'+str(self.file.tell())
        header = struct.unpack('<IIII',self.file.read(self.capHeaderLen))
        #print dict(zip(self.capStructure,header))
        return dict(zip(self.capStructure,header))
    def next(self):
        try:
            self.file.seek(self.current,0)
            self.previous = self.current
            cap = self.capHeader()
            capLen = cap.get('capLen')
            self.current += capLen+self.capHeaderLen
            #print 'tell: (after)'+str(self.file.tell())
            #['time','len','loc']
            info = [float(str(cap.get('gmtTime'))+'.'+str(cap.get('microTime'))), capLen, self.previous]
            return info
        except struct.error:
            raise StopIteration
    def __iter__(self):
        return self
    def close(self):
        self.file.close()

def getInfo(fn):
    info = []
    try:
        if os.path.isfile(fn):
            cap = PCAP(fn)
            try:
                if cap.isPCAP():
                    for frame in cap:
                        frame.append(fn)
                        info.append(frame)
            finally: cap.close()
        else:
            raise IOError
    except Exception, e:
        logException()
        #print e
    return info

def sortInfo(fns):
    #['time','size','location','file_name']
    res = []
    for fn in fns:
        res += getInfo(fn)
    res.sort()
    return res

def genName(fns):
    names = []
    name = ''
    for fn in fns:
        names.append(int(re.split(r'[,|\.]', os.path.split(fn)[-1])[0]))
    names.sort()
    for n in names:
        name += str(n)+'.'
    temp = time.strftime('%Y%m%d.%H%M%S',time.localtime(time.time()))
    return name+temp+'.pcap'

def mergePCAP(fns, name='merged.pcap'):
    res = sortInfo(fns)
    fo = dict()
    try:
        try:
        #with open(name, 'wb') as f:
            f = open(name, 'wb')
            for fn in fns:
                fo[fn] = open(fn,'rb')
            try:
                f.write(fo[fns[0]].read(PCAP.headerLen))
                for line in res:
                    fo[line[3]].seek(line[2])
                    packet = fo[line[3]].read(line[1]+PCAP.capHeaderLen)
                    f.write(packet)
            finally:
                for fn in fns:
                    fo[fn].close()
        finally: f.close()
    except Exception:
        if os.path.isfile(name) and not os.path.getsize(name):
            os.remove(name)
            #print 'del '+name
            logException()
        name = 0
    return name

def isPCAP(fn):
    #with open(fn) as f:
    f = open(fn)
    try:
        f.seek(0,0)
        magic = f.read(PCAP.magicLen)
    finally: f.close()
    return magic == '\xd4\xc3\xb2\xa1' or magic == '\xa1\xb2\xc3\xd4'

def rmPCAP(duration = 24, dir = '.'):
    """unit is hour"""
    duration *= 3600
    count = 0
    for fn in os.listdir(dir):
        fn = join(dir,fn)
        cTime = os.stat(fn).st_ctime
        if isPCAP(fn) and (time.time()-cTime) > duration:
            os.remove(fn)
            count += 1
    return count

def __merged(fns, name='merged', mode='b', header_len=0):
    if mode != 'b': mode = ''
    if os.path.isfile(name): os.remove(name)
    count = 0
    #with open(name, 'a'+mode) as f:
    f = open(name, 'a'+mode)
    try:
        for file in fns:
            if os.path.isfile(file):
                count += 1
                if count == 1:
                    ff = open(file, 'r'+mode)
                    f.write(ff.read())
                else:
                    ff = open(file, 'r'+mode)
                    ff.seek(header_len, 0)
                    f.write(ff.read())
                print file
            else:
                print file+' is not exist'
    finally: f.close()
    print '='*25
    print 'Successfully merged '+str(count)+' files'
    print 'Merged file is '+name

if __name__ == '__main__':

    fns = [r'pcap\16.20130103.2312.ISC.qln02',
           r'pcap\18.20130103.2333.ISC.qln02',
           r'pcap\19.20130104.0033.ISC.qln02']
    #cap = PCAP(r'pcap\3.20130104.2034.ISC.qln02')
    #print cap.next()

    #info = getInfo(fns[0])
    #pprint(info)

    #cap = PCAP(fns[0])
    ##print cap.sip(1383,1584)
    #for frame in getInfo(fns[0]):
    #    print cap.sip(frame[1], frame[2])

    #__merge(filelist, name='merged.pcap', header_len=24)

    #pprint(sortInfo(fns))
    #print mergePCAP(fns,name=join('pcap',genName(fns)))
    #print mergePCAP(fns)

    #print rmPCAP(duration = 24, dir='pcap')
    #print genName(fns)

    if len(sys.argv)>2:
        fns = sys.argv[1:]
        print mergePCAP(fns,genName(fns))




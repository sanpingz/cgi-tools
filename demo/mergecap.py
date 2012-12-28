__author__ = 'sanpingz'

import os, struct

class PCAP:
    headerLen = 24
    capHeaderLen = 16
    capStruct = ['GMTtime','microTime','capLen','len']
    def __init__(self, fn):
        self.file = open(fn, 'rb')
        self.file.seek(self.headerLen)
        self.current = self.headerLen
    def getHeader(self):
        now = self.file.tell()
        self.file.seek(0)
        header = self.file.read(self.headerLen)
        self.file.seek(now)
        return header
    def capHeader(self):
        return self.file.read(self.capHeaderLen)
    def getUnpackedCapHeader(self):
        header = struct.unpack('IIII',self.capHeader())
        print self.file.tell()
        return dict(zip(self.capStruct,header))
    def hasNext(self):
        flag = False
        if self.capHeader():
            flag = True
        return flag
    def next(self):
        if self.file.readable():
            capLen = self.getUnpackedCapHeader().get('capLen')
            self.current += capLen
            #self.file.seek(self.current)
            return self.current
        else:
            raise StopIteration
    def __iter__(self):
        return self
    def close(self):
        self.file.close()


def merge(filelist, name='merged', mode='b', header_len=0):
    if mode != 'b': mode = ''
    if os.path.isfile(name): os.remove(name)
    count = 0
    with open(name, 'a'+mode) as f:
        for file in filelist:
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
    print '='*25
    print 'Successfully merged '+str(count)+' files'
    print 'Merged file is '+name

if __name__ == '__main__':

    filelist = ['56,20121123.0233,ISC.gll14',
                '60,20121125.2131,ISC.gll14',
                '66,20121126.1917,ISC.gll14']
    #merge(filelist, name='merged.pcap', header_len=24)
    cap = PCAP('60,20121125.2131,ISC.gll14')
    print cap.getUnpackedCapHeader()
    for frame in cap:
        print frame
    cap.close()



__author__ = 'sanpingz'

import os, struct

def getInfo(fn):
    cap = PCAP(fn)
    info = []
    for frame in cap:
        print frame
    cap.close()
class PCAP:
    headerLen = 24
    capHeaderLen = 16
    capStruct = ['gmtTime','microTime','capLen','len']
    def __init__(self, fn):
        self.file = open(fn, 'rb')
        #self.file.seek(self.headerLen,0)
        self.previous = 0
        self.current = self.headerLen
    def header(self):
        now = self.file.tell()
        self.file.seek(0)
        header = self.file.read(self.headerLen)
        self.file.seek(now)
        return header
    def capHeader(self):
        #print 'tell: (before)'+str(self.file.tell())
        header = struct.unpack('IIII',self.file.read(self.capHeaderLen))
        #print dict(zip(self.capStruct,header))
        return dict(zip(self.capStruct,header))
    def next(self):
        try:
            self.file.seek(self.current,0)
            self.previous = self.current
            cap = self.capHeader()
            capLen = cap.get('capLen')
            self.current += capLen+self.capHeaderLen
            #print 'tell: (after)'+str(self.file.tell())
            res = ['time','len','loc']
            info = [float(str(cap.get('gmtTime'))+'.'+str(cap.get('microTime'))), capLen, self.previous]
            return dict(zip(res,info))
        except struct.error:
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

    print getInfo('60,20121125.2131,ISC.gll14')


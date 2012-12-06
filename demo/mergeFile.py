__author__ = 'sanpingz'

import os

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
    merge(filelist, name='merged.pcap', header_len=24)


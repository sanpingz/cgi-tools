#!/opt/exptools/bin/python
__author__ = 'sanpingz'

from os.path import join, abspath
import sys, os
import pickle, shutil

BASE_DIR = ''
config = {'dirname':'data',
          'logname':'log',
          'pcapdir':'pcap',
          'ctname':'ctid.dat'
}
def init():
    if os.path.exists(config['dirname']):
        shutil.rmtree(config['dirname'])
    if os.path.exists(config['logname']):
        shutil.rmtree(config['logname'])
    if os.path.exists(config['pcapdir']):
        shutil.rmtree(config['pcapdir'])
    try:
        os.mkdir(config['dirname'])
        print config['dirname']+' created'
        os.mkdir(config['logname'])
        print config['logname']+' created'
        os.mkdir(config['pcapdir'])
        print config['pcapdir']+' created'
    except Exception, e:
        print e
    BASE_DIR = abspath(config['dirname'])
    filepath = join(BASE_DIR, config['ctname'])
    ctid = 0
    file = open(filepath, 'wb')
    try:
        pickle.dump(ctid, file)
        print 'trace ID reset'
    except Exception, e:
        print e
    file.close()
    try:
        os.system('chmod 777 '+config['dirname'])
        os.system('chmod 777 '+config['logname'])
        os.system('chmod 777 '+config['pcapdir'])
        os.system('chmod 777 '+filepath)
        print 'file permissions modified'
    except Exception, e:
        print e

if __name__ == '__main__':
    init()
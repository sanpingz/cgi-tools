#!/opt/x11r6/bin/python
__author__ = 'sanpingz'

from os.path import join, abspath
import sys, os
import pickle

BASE_DIR = ''
config = {'dirname':'data',
          'ctname':'ctid.dat'
}
def init():
    try:
        os.mkdir(config['dirname'])
    except Exception, OSError:
        pass
    BASE_DIR = abspath(config['dirname'])
    filepath = join(BASE_DIR, config['ctname'])
    ctid = 0
    file = open(filepath, 'wb')
    try:
        pickle.dump(ctid, file)
    except Exception, OSError:
        pass
    file.close()
    os.system('chmod 777 '+filepath)

if __name__ == '__main__':
    init()
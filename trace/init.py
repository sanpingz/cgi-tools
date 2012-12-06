#!/opt/exptools/bin/python
__author__ = 'sanpingz'

from os.path import join, abspath
import os, shelve
import shutil

BASE_DIR = ''
config = {'dir':'data',
          'log':'log',
          'db':'tracedb'
}
TELNUM = '''<Request Action="STARTCT">
                <CallTraceCli>
                    <CTID>(ctid)</CTID>
                    <APPTYPE>(apptype)</APPTYPE >
                    <TELNUMMATCH>
                        <(mode)>(callid)</(mode)>
                        <MATCHDIR>(matchdir)</MATCHDIR>
                    </TELNUMMATCH>
                    <DURATION>(duration)</DURATION>
                </CallTraceCli>
            </Request>'''
SIPURI = '''<Request Action="STARTCT">
                <CallTraceCli>
                    <CTID>(ctid)</CTID>
                    <APPTYPE>(apptype)</APPTYPE >
                    <(mode)>(callid)</(mode)>
                    <DURATION>(duration)</DURATION>
                </CallTraceCli>
            </Request>'''
STOP = '''<Request Action="TERMCT">
        <CallTraceCli>
        <CTID>(ctid)</CTID>
        <APPTYPE>(apptype)</APPTYPE >
        </CallTraceCli>
        </Request>'''
def init():
    if os.path.exists(config['dir']):
        shutil.rmtree(config['dir'])
    if os.path.exists(config['log']):
        shutil.rmtree(config['log'])
    try:
        os.mkdir(config['dir'])
        os.mkdir(config['log'])
    except Exception, e:
        print 'init directory failed'
        print e
    BASE_DIR = abspath(config['dir'])
    file = join(BASE_DIR, config['db'])
    db = shelve.open(file)
    try:
        db['_ctid'] = 0
        db['_TELNUM'] = TELNUM
        db['_SIPURI'] = SIPURI
        db['_STOP'] = STOP
    except Exception, e:
        print 'init DB failed'
        print e
    db.close()
    os.system('chmod 777 '+config['dir'])
    os.system('chmod 777 '+config['log'])
    os.system('chmod 755 '+file)

if __name__ == '__main__':
    init()
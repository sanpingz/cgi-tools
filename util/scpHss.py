#!/usr/bin/env python
"""usage: scpHSS CNFG_IP"""
__author__ = 'sanpingz(sanping.zhang@alcatel-lucent)'

import sys, getopt, os, re, ftplib
from simpleFTP import sFTP

HSS_DIR = r'/home/sanpingz/hss'

def getName():
    return re.findall(r'\w+', os.popen('who am i').read())[0]

def ftpLab(cnfg_ip):
    try:
        ftp = sFTP(host=cnfg_ip, timeout=6)
        ftp.login(user='lss', passwd='lss')
        #ftp.set_debuglevel(2)
        print ftp.getwelcome()
        ftp.cwd(r'/storage')
        name = getName()
        try:
            ftp.cwd(name)
            print r'/storage/'+name+r' is exist'
        except ftplib.error_perm:
            ftp.mkd(name)
            print 'created sanpingz'
            ftp.cwd(name)
        try:
            ftp.cwd('hss')
            print r'/storage/'+name+r'/hss is exist'
        except ftplib.error_perm:
            ftp.mkd('hss')
            print 'created hss'
            ftp.cwd('hss')
        ftp.mput(HSS_DIR)
        #ftp.set_debuglevel(0)
    except Exception, e:
        print e
    finally:
        try:
            ftp.quit()
            ftp.close()
        except: pass
def test():
    ftp = sFTP(host='135.252.226.50', timeout=6)
    ftp.login(user='lss', passwd='lss')
    ftp.cwd(r'/storage/sanpingz')
    ftp.put(r'simpleFTP.py')
    ftp.quit()
    ftp.close()


if __name__ == '__main__':
    #getopt.gnu_getopt(sys.argv[1:], )
    if len(sys.argv)>1:
        ftpLab(sys.argv[1])
    else:
        print __doc__


#!/usr/bin/env python
"""usage: scp_hss CNFG_IP"""
__author__ = 'sanpingz(sanping.zhang@alcatel-lucent)'

import sys, getopt, os, re
from simpleFTP import sFTP

HSS_DIR = r'/home/sanpingz/hss'

def getName():
    return re.findall(r'\w+', os.popen('who am i').read())[0]

def ftpLab(cnfg_ip):
    try:
        ftp = sFTP(host=cnfg_ip, timeout=10)
        ftp.login(user='lss', passwd='lss')
        ftp.set_debuglevel(2)
        print ftp.getwelcome()
        ftp.cwd(r'/storage')
        name = getName()
        if ftp.isdir(name):
            print r'/storage/'+name+'is exist'
        else:
            ftp.mkd(name)
            print 'created '+name
        ftp.cwd(name)
        if ftp.isdir('hss'):
            print r'/storage/'+name+r'/hss is exist'
            ftp.rmdir('hss')
        ftp.mkd('hss')
        print 'created hss'
        ftp.put(HSS_DIR)
        ftp.set_debuglevel(0)
    except Exception, e:
        print e
    finally:
        ftp.quit()


if __name__ == '__main__':
    #getopt.gnu_getopt(sys.argv[1:], )
    ftpLab(sys.argv[1])


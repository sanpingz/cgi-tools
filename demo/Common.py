#!/opt/exptools/bin/python
__author__ = 'sanpingz'

import pexpect, os, sys

def scp(addr,passwd,dest):
    cmd = 'scp '+addr+' '+dest
    if os.path.exists(dest):
        log=open('log.txt','a')
        child = pexpect.spawn(cmd)
        index = child.expect(['Password:',r'yes/no', pexpect.EOF,pexpect.TIMEOUT], timeout=30)
        if index == 0:
            child.sendline(passwd)
        elif index == 1:
            child.sendline('yes')
            child.expect('Password:')
            child.sendline(passwd)
        elif index == 2:
            print 'EOF'
        elif index == 3:
            print 'Timeout'
        if child.isalive():
            child.close()
        log.close()


if __name__ == '__main__':
    addr = r'lss@135.252.226.34:/logs/ctlog/142.20121226.0053.ISC.qln02'
    print os.path.join(r'pcap',os.path.split(addr)[1])
    scp(addr,'lss',r'pcap/')


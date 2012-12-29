#!/usr/bin/env python
"""usage: genFile(.py) filename type{SIP, Dia} size"""
__author__ = 'sanpingz(sanping.zhang@alcatel-lucent)'

import sys, os

sip_temp = '''\
source SIPUA.tcl
source SIPpAS.tcl
source SIPb2bAS.tcl
set proxyhost 135.252.226.38
set proxyport 5060
set realm ate.lucentlab.com

catch { delete obj ua1}
SIPUA ua1 ua1 -myaddress sip:+15351100001@${realm} -proxyhost ${proxyhost} -proxyport ${proxyport} -uaport 24001 -privateid privateid01@${realm} -realm ${realm} -passwd newsys
puts "ua1 created\\n"
ua1 configure -noAnswer ""

catch { delete obj ua2}
SIPUA ua2 ua2 -myaddress sip:+15351100002@${realm} -proxyhost ${proxyhost} -proxyport ${proxyport} -uaport 24002 -privateid privateid02@${realm} -realm ${realm} -passwd newsys
puts "ua2 created\\n"
ua2 configure -noAnswer "yes"
ua2 configure -SDP180 "v=0
o=- 173280590 993967093 IN IP4 135.252.30.44
s=-
c=IN IP4 135.252.30.44
t=0 0
m=audio 5006 RTP/AVP 8 3 0
'''
dia_temp = '17,<InitialFilterCriteria><Priority>0</Priority><TriggerPoint><ConditionTypeCNF>1</ConditionTypeCNF><SPT><ConditionNegated>0</ConditionNegated><Group>1</Group><Method>INVITE</Method></SPT></TriggerPoint><ApplicationServer><ServerName>sip:10.201.64.16:22190</ServerName><DefaultHandling>0</DefaultHandling></ApplicationServer></InitialFilterCriteria>'

sip_rep = 'a=rtpmap:0 PCMU/8000'
dia_rep = '<SPT><ConditionNegated>0</ConditionNegated><Group>1</Group><Method>INVITE</Method></SPT>'
dia_app = '<ApplicationServer><ServerName>sip:10.201.64.16:22190</ServerName><DefaultHandling>0</DefaultHandling></ApplicationServer>'

sip_size = len(sip_temp)
dia_size = len(dia_temp)

class Generator:
    def __init__(self, name, type, size):
        self.name = name
        self.type = type.lower()
        self.size = int(size)
    def genSIP(self):
        if self.size < sip_size: raise Exception, 'size too small'
        f = open(self.name, 'wb')
        try:
            f.write(sip_temp)
            length = len(sip_rep)
            num = sip_size
            while num <= self.size:
                f.write(sip_rep + '\n')
                num += (length+1)
            f.write('"')
            print 'message size is ',num+1
        #except Exception:
        #    print 'file write error'
        finally:
            f.close()
    def genDia(self):
        if self.size < dia_size: raise Exception, 'size too small'
        f = open(self.name, 'wb')
        try:
            length = len(dia_rep)
            start = dia_temp.index(dia_rep)
            num = dia_size
            f.write(dia_temp[:start])
            count = 1
            while num <= self.size and count < 15:
                f.write(dia_rep)
                num += length
                count += 1
            start_app = dia_temp[start:].index(dia_app)
            length_app = len(dia_app)
            f.write(dia_temp[start:][:start_app])
            while num <= self.size:
                f.write(dia_app)
                num += length_app
            f.write(dia_temp[start:][start_app:])
            print 'message size is ',num
        #except Exception, e:
        #    print 'file write error, ', e
        finally:
            f.close()
    def gen(self):
        try:
            if self.type.lower()=='sip':
                self.genSIP()
            elif self.type.lower()=='dia':
                self.genDia()
            print self.name+' file wrote successfully'
            os.system('chmod 755 '+self.name)
        except Exception, e:
            print e
            print self.name+' file wrote error'

if __name__ == '__main__':
    print __doc__
    if len(sys.argv) < 4:
        print 'lack of parameters, try again'
        sys.exit()
    try:
        fname = sys.argv[1]
        ftype = sys.argv[2]
        fsize = sys.argv[3]
    except Exception, e:
        print e
        print 'parameter error, try again'
    else:
        if ftype.lower()!='sip' and ftype.lower()!='dia':
            print 'file type error, only SIP or Dia is valid'
        elif not fsize.isdigit():
            print 'file size error, file size is digit'
        else:
            print 'file name : ' + fname
            print 'file type : ' + ftype
            print 'file size : ' + fsize

            print '-'*20
            gt = Generator(fname, ftype, fsize)
            gt.gen()
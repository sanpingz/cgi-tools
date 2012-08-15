#!/opt/x11r6/bin/python
from os.path import join, abspath
import os
from exceptions import Exception
import pickle
from string import replace

BASE_DIR = abspath('data')
hostParam = {'port':'9623'
}
class startCall:
    status = 'Started'
    error = {}
    def __init__(self, duration, mode, labip):
        self.duration = duration
        self.mode = mode
        self.labip = labip
    def setCallId(self, callid, matchdir="Right"):
        self.callid = callid
        self.matchdir = matchdir
    def __setTemplate__(self):
        template = ''
        if 'TELNUM' == self.mode:
            template = '''<Request Action="STARTCT">
                <CallTraceCli>
                    <CTID>(ctid)</CTID>
                    <TELNUMMATCH>
                        <(mode)>(callid)</(mode)>
                        <MATCHDIR>(matchdir)</MATCHDIR>
                    </TELNUMMATCH>
                    <DURATION>(duration)</DURATION>
                </CallTraceCli>
            </Request>'''
        else:
            template = '''<Request Action="STARTCT">
                <CallTraceCli>
                    <CTID>(ctid)</CTID>
                    <(mode)>(callid)</(mode)>
                    <DURATION>(duration)</DURATION>
                </CallTraceCli>
            </Request>'''
        return template
    def __getCtid__(self):
        ctid = 0
        filepath = join(BASE_DIR, 'ctid.dat')
        f = open(filepath, 'rb')
        try:
            ctid = pickle.load(f)
        finally: f.close()
        return ctid
    def __setCtid__(self):
        filepath = join(BASE_DIR, 'ctid.dat')
        ctid = self.__getCtid__()+1
        if ctid >= 16777216:
            ctid = 0
        self.ctid = str(ctid)
        f = open(filepath, 'wb')
        try:
            pickle.dump(ctid, f)
        finally: f.close()
    def createXML(self):
        self.__setCtid__()
        filename = 'start'+str(self.ctid)+'.xml'
        filepath = join(BASE_DIR, filename)
        template = self.__setTemplate__()
        template = replace(template, '(ctid)', self.ctid)
        template = replace(template, '(mode)', self.mode)
        template = replace(template, '(callid)', self.callid)
        template = replace(template, '(duration)', self.duration)
        if 'TELNUM' == self.mode:
            template = replace(template, '(matchdir)', self.matchdir)
        f = open(filepath, 'w')
        try:
            f.write(template)
        except Exception:
            self.status = 'Failure'
            self.error['createXML'] = 'start.xml create failed'
            #print filename+' create failed'
        else:
            #print filename+' created successfully'
            os.system('chmod 755 '+filepath)
        f.close()
    def startCommand(self):
        if 'Started' == self.status:
            ctid = str(self.ctid)
            input = 'data/start'+ctid+'.xml'
            cmm = './xml2cfg'
            labip = str(self.labip)
            out = 'data/out'+ctid+'.xml'
            command =cmm+' -h '+labip+' -p '+hostParam['port']+' -i '+input+' -o '+out
            try:
                os.system(command)
                os.remove(input)
                os.remove(out)
            except OSError, Exception:
                self.status = 'Failure'
                self.error['startCommand'] = 'command execute error'
                #print 'command execute error'
            else:
                pass
                #print command

class stopCall:
    status = 'Stopped'
    error = {}
    def __init__(self, labip, ctid=''):
        self.labip = labip
        self.ctid = ctid
    def createXML(self):
        filename = 'stop'+str(self.ctid)+'.xml'
        filepath = join(BASE_DIR, filename)
        template = '''<Request Action="TERMCT">
        <CallTraceCli>
        <CTID>(ctid)</CTID>
        </CallTraceCli>
        </Request>'''
        template = replace(template, '(ctid)', self.ctid)
        f = open(filepath, 'w')
        try:
            f.write(template)
        except Exception:
            self.status = 'Failure'
            self.error['createXML'] = 'stop.xml create failed'
        else:
            os.system('chmod 755 '+filepath)
        f.close()
    def startCommand(self):
        if 'Stopped' == self.status:
            ctid = str(self.ctid)
            input = 'data/stop'+ctid+'.xml'
            cmm = './xml2cfg'
            labip = str(self.labip)
            out = 'data/out'+ctid+'.xml'
            command =cmm+' -h '+labip+' -p '+hostParam['port']+' -i '+input+' -o '+out
            try:
                os.system(command)
                os.remove(input)
                os.remove(out)
            except OSError, Exception:
                self.status = 'Failure'
                self.error['startCommand'] = 'command execute error'

def startCallTrace(param):
    start = startCall(duration=param['duration'], mode=param['mode'], labip=param['labip'])
    if 'TELNUM' == param['mode']:
        start.setCallId(callid=param['callid'], matchdir=param['matchdir'])
    else:
        start.setCallId(callid=param['callid'])
    start.createXML()
    start.startCommand()

def stopCallTrace(param):
    stop = stopCall(labip=param['labip'], ctid=param['ctid'])
    stop.createXML()
    stop.startCommand()

if __name__ == '__main__':

    start = {'duration':'30',
             'labip':'135.2.121.97',
             'mode':'TELNUM',
             'callid':'18753251981',
             'matchdir':'Right'
    }
    #startCallTrace(start)

    stop = {'labip':'135.2.121.97',
            'ctid':''
    }
    stopCallTrace(stop)

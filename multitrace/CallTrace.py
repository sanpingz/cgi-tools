#!/opt/exptools/bin/python
from os.path import join
import os, time, glob
from exceptions import Exception
import pickle
from string import replace
from JsonDB import simpleDB
import SimpleFTP
from TimeFunc import FuncWrapper, Timeout
from logCtrl import simpleLog

BASE_DIR = 'data'
LOCAL = 'pcap'
HOST_PORT = '9623'
LOG_FILE = join(BASE_DIR, 'calltrace.log')
template_TELNUM = '''<Request Action="STARTCT">
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
template_SIPURI = '''<Request Action="STARTCT">
    <CallTraceCli>
        <CTID>(ctid)</CTID>
        <APPTYPE>(apptype)</APPTYPE >
        <(mode)>(callid)</(mode)>
        <DURATION>(duration)</DURATION>
    </CallTraceCli>
</Request>'''
template_STOP = '''<Request Action="TERMCT">
    <CallTraceCli>
    <CTID>(ctid)</CTID>
    <APPTYPE>(apptype)</APPTYPE >
    </CallTraceCli>
</Request>'''

def logException():
    simpleLog(name='calltrace', file=LOG_FILE)

class callTrace:
    def __init__(self, param):
        self.error = {}
        self.status = ''
        self.labip = param['labip']
        self.apptype = param.get('apptype')
        self.handle = param.get('handle')
        self.ctid = 0
    def setApptype(self):
        if 'IMS' == self.apptype:
            self.apptype = 'SC,IBC4'
        elif 'FS5K' == self.apptype:
            self.apptype = 'CTS,SCG'
        else:
            self.apptype = 'SC,IBC4,CTS,SCG'
    def isMulti(self):
        return isinstance(self.labip, list)
    def createXML(self): pass
    def exeCommand(self, labip):
        ctid = str(self.ctid)
        input = join('data','start'+ctid+'.xml')
        cmm = './xml2cfg'
        out = join('data','out'+ctid+'.xml')
        #command =cmm+' -h '+labip+' -p '+HOST_PORT+' -i '+input+' -o '+out
        command ='%s -h %s -p %s -i %s -o %s' % (cmm, labip, HOST_PORT, input, out)
        try:
            os.system(command)
        except Exception:
            self.status = 'Failure'
            self.error['exeCommand'] = 'command execute error on '+labip
            logException()
    def safeCommand(self, labip):
        ctid = str(self.ctid)
        input = join('data','start'+ctid+'.xml')
        cmm = './xml2cfg'
        out = join('data','out'+ctid+'.xml')
        command =cmm+' -h '+labip+' -p '+HOST_PORT+' -i '+input+' -o '+out
        func_obj = FuncWrapper(os.system, command)
        try:
            t = Timeout(8, func_obj)
            t.run()
            cb = func_obj.result
        except Exception:
            self.status = 'Failure'
            self.error['startCommand'] = 'command execute error on '+labip
            logException()
        else:
            if cb : self.status = 'Failure'
    def startCommand(self):
        if 'Failure' != self.status:
            try:
                if self.isMulti():
                    for ip in self.labip:
                        self.exeCommand(ip)
                else:
                    self.exeCommand(self.labip)
            finally:
                xml = glob.glob(join('data',r'*.xml'))
                if xml:
                    for x in xml:
                        os.remove(x)

class startCall(callTrace):
    def __init__(self, param):
        callTrace.__init__(self, param)
        self.status = 'Started'
        self.duration = param['duration']
        self.mode = param['mode']
        self.callid = param['callid']
        self.matchdir = param.get('matchdir')
    def __setTemplate(self):
        template = template_SIPURI
        if 'TELNUM'==self.mode:
            template = template_TELNUM
        return template
    def __getCtid(self):
        ctid = 0
        filepath = join(BASE_DIR, 'ctid.dat')
        f = open(filepath, 'rb')
        try:
            ctid = pickle.load(f)
        finally: f.close()
        return ctid
    def __setCtid(self):
        filepath = join(BASE_DIR, 'ctid.dat')
        ctid = self.__getCtid()+1
        if ctid >= 16777216:
            ctid = 0
        self.ctid = str(ctid)
        f = open(filepath, 'wb')
        try:
            pickle.dump(ctid, f)
        finally: f.close()
    def createXML(self):
        self.__setCtid()
        filename = 'start'+str(self.ctid)+'.xml'
        filepath = join(BASE_DIR, filename)
        self.setApptype()
        template = self.__setTemplate()
        template = replace(template, '(ctid)', self.ctid)
        template = replace(template, '(mode)', self.mode)
        template = replace(template, '(callid)', self.callid)
        template = replace(template, '(apptype)', self.apptype)
        template = replace(template, '(duration)', self.duration)
        if 'TELNUM' == self.mode:
            template = replace(template, '(matchdir)', self.matchdir)
        f = open(filepath, 'w')
        try:
            f.write(template)
        except Exception:
            self.status = 'Failure'
            self.error['createXML'] = 'start.xml create failed'
            logException()
        f.close()
        os.system('chmod 755 '+filepath)
    def saveData(self):
        user = {}
        param = {}
        if self.status == 'Started' and self.handle:
            sd = simpleDB(self.handle)
            TIMEFORMAT = '%Y-%m-%d %X'
            cnt = time.time()+time.altzone+8*3600
            startime = time.strftime(TIMEFORMAT, time.localtime(cnt))
            param['ctid'] = self.ctid
            param['duration'] = self.duration
            param['mode'] = self.mode
            param['labip'] = self.labip
            param['callid'] = self.callid
            param['apptype'] = self.apptype
            param['matchdir'] = self.matchdir
            param['startime'] = startime
            param['time'] = time.time()
            param['status'] = self.status
            user[str(self.ctid)] = param
            sd.add(user)

class stopCall(callTrace):
    def __init__(self, param):
        callTrace.__init__(self, param)
        self.status = 'Stopped'
        self.ctid = param['ctid']
    def createXML(self):
        filename = 'stop'+str(self.ctid)+'.xml'
        filepath = join(BASE_DIR, filename)
        template = template_STOP
        self.setApptype()
        template = replace(template, '(ctid)', self.ctid)
        template = replace(template, '(apptype)', self.apptype)
        f = open(filepath, 'w')
        try:
            f.write(template)
        except Exception:
            self.status = 'Failure'
            self.error['createXML'] = 'stop.xml create failed'
            logException()
        f.close()
        os.system('chmod 755 '+filepath)
    def updateData(self):
        if self.status == 'Stopped' and self.handle:
            db = simpleDB(self.handle)
            user = db.select(self.ctid)
            data = dict()
            param = SimpleFTP.parameter
            param['local'] = LOCAL
            param['labip'] = user['labip']
            param['ctid'] = user['ctid']
            addr = SimpleFTP.addr(param=param)
            if addr and len(addr)<120:
                user['status'] = 'Stopped'
                user['addr'] = addr
            else:
                user['status'] = 'Failure'
            data[self.ctid] = user
            db.update(data)

def toString(lt):
    res = ''
    if lt and isinstance(lt,list):
        for item in lt:
            res += item+','
        res = res[:-1]
    else:
        res = lt
    return res

def exeCallTrace(aClass,param):
    ct = aClass(param)
    ct.createXML()
    ct.startCommand()

if __name__ == '__main__':

    param = {'duration':'30',
             'labip':'135.252.226.34',
             'mode':'TELNUM',
             'apptype':'All',
             'callid':'18753251981',
             'matchdir':'Right',
             'handle':'sanpingz',
             'ctid':0
    }
    exeCallTrace(startCall, param)
    #exeCallTrace(stopCall, param)


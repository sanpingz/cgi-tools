#!/opt/exptools/bin/python
from os.path import join, abspath
import os, time
from exceptions import Exception
import pickle, shelve
from string import replace
from JsonDB import simpleDB
import SimpleFTP
from TimeFunc import FuncWrapper, Timeout

BASE_DIR = abspath('data')
hostParam = {'port':'9623'
}
LOCAL = 'pcap'
class startCall:
    status = 'Started'
    error = {}
    def __init__(self, param):
        self.duration = param['duration']
        self.mode = param['mode']
        self.labip = param['labip']
        self.callid = param['callid']
        self.apptype = param.get('apptype')
        self.matchdir = param.get('matchdir')
        self.handle = param.get('handle')
    def __setApptype(self):
        if 'IMS' == self.apptype:
            self.apptype = 'SC,IBC4'
        elif 'FS5K' == self.apptype:
            self.apptype = 'CTS,SCG'
        else:
            self.apptype = 'SC,IBC4,CTS,SCG'
    def __setTemplate(self):
        template = ''
        if 'TELNUM' == self.mode:
            template = '''<Request Action="STARTCT">
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
        else:
            template = '''<Request Action="STARTCT">
                <CallTraceCli>
                    <CTID>(ctid)</CTID>
                    <APPTYPE>(apptype)</APPTYPE >
                    <(mode)>(callid)</(mode)>
                    <DURATION>(duration)</DURATION>
                </CallTraceCli>
            </Request>'''
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
        self.__setApptype()
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
            #print filename+' create failed'
        f.close()
        os.system('chmod 755 '+filepath)
    def startCommand(self):
        if 'Started' == self.status:
            ctid = str(self.ctid)
            input = 'data/start'+ctid+'.xml'
            cmm = './xml2cfg'
            labip = str(self.labip)
            out = 'data/out'+ctid+'.xml'
            command =cmm+' -h '+labip+' -p '+hostParam['port']+' -i '+input+' -o '+out
            func_obj = FuncWrapper(os.system, command)
            try:
                t = Timeout(8, func_obj)
                timer = time.time()
                t.run()
                timer = time.time()-timer
                #print timer
                cb = func_obj.result
                if os.path.exists(input): os.remove(input)
                if os.path.exists(out): os.remove(out)
            #except WindowsError: pass
            except Exception:
                self.status = 'Failure'
                self.error['startCommand'] = 'command execute error'
                raise Exception("CMDError")
                #cb = os.system(command)
            else:
                if cb : self.status = 'Failure'
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

class stopCall:
    status = 'Stopped'
    error = {}
    def __init__(self, param):
        self.labip = param['labip']
        self.ctid = param['ctid']
        self.apptype = param.get('apptype')
        self.handle = param.get('handle')
    def __setApptype(self):
        if 'IMS' == self.apptype:
            self.apptype = 'SC,IBC4'
        elif 'FS5K' == self.apptype:
            self.apptype = 'CTS,SCG'
        else:
            self.apptype = 'SC,IBC4,CTS,SCG'
    def createXML(self):
        filename = 'stop'+str(self.ctid)+'.xml'
        filepath = join(BASE_DIR, filename)
        template = '''<Request Action="TERMCT">
        <CallTraceCli>
        <CTID>(ctid)</CTID>
        <APPTYPE>(apptype)</APPTYPE >
        </CallTraceCli>
        </Request>'''
        self.__setApptype()
        template = replace(template, '(ctid)', self.ctid)
        template = replace(template, '(apptype)', self.apptype)
        f = open(filepath, 'w')
        try:
            f.write(template)
        except Exception:
            self.status = 'Failure'
            self.error['createXML'] = 'stop.xml create failed'
        f.close()
        os.system('chmod 755 '+filepath)
    def startCommand(self):
        if 'Stopped' == self.status:
            ctid = str(self.ctid)
            input = 'data/stop'+ctid+'.xml'
            cmm = './xml2cfg'
            labip = str(self.labip)
            out = 'data/out'+ctid+'.xml'
            command =cmm+' -h '+labip+' -p '+hostParam['port']+' -i '+input+' -o '+out
            try:
                cb = os.system(command)
                if cb: self.status = 'Failure'
                os.remove(input)
                os.remove(out)
            except OSError, Exception:
                self.status = 'Failure'
                self.error['startCommand'] = 'command execute error'
    def updateData(self):
        if self.status == 'Stopped' and self.handle:
            db = simpleDB(self.handle)
            user = db.select(self.ctid)
            data = dict()
            param = SimpleFTP.parameter
            param['host'] = user['labip']
            param['local'] = LOCAL
            ctid = user['ctid']
            addr = SimpleFTP.addr(ctid,param=param)
            if addr and len(addr)<120:
                user['status'] = 'Stopped'
                user['addr'] = addr
            else:
                user['status'] = 'Failure'
            data[self.ctid] = user
            db.update(data)

def startCallTrace(param):
    start = startCall(param)
    start.createXML()
    start.startCommand()

def stopCallTrace(param):
    stop = stopCall(param)
    stop.createXML()
    stop.startCommand()

if __name__ == '__main__':

    start = {'duration':'30',
             'labip':'135.2.121.97',
             'mode':'TELNUM',
             'apptype':'All',
             'callid':'18753251981',
             'matchdir':'Right'
    }
    startCallTrace(start)

    stop = {'labip':'135.2.121.97',
            'ctid':'',
            'apptype':'All',
            'handle':''
    }
    #stopCallTrace(stop)

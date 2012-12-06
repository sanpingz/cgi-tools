#!/opt/exptools/bin/python
__author__ = 'sanpingz'

from ftplib import FTP
import re

parameter = {'host':'135.2.121.97',
         'user':'lss',
         'passwd':'lss',
         'cwd':'../../../logs/ctlog',
         'ctid':'99'
}
class ftpDownload:
    def __init__(self,param):
        self.host = param['host']
        self.user = param['user']
        self.passwd = param['passwd']
        self.cwd = param['cwd']
        self.ctid = param['ctid']
    def getFileList(self):
        try:
            ftp = FTP(self.host)
            ftp.login(self.user, self.passwd)
            ftp.cwd(self.cwd)
        except : return ''
        else: return ftp.nlst()
    def matchFile(self):
        matched = ''
        num = 0
        filelist = self.getFileList()
        reg = str(self.ctid)+r',\d{8}\.\d{4}\,ISC\.\w{3,}'
        pattern = re.compile(reg)
        if filelist:
            for file in filelist:
                if pattern.match(file) and int(re.split('[,|.]+',file)[2])>num:
                    matched = file
                    num = int(re.split('[,|.]+',file)[2])
        return  matched
    def getAddr(self):
        file = self.matchFile()
        if file:
            addr = r'ftp://'+self.user+':'+self.passwd+'@'+self.host+r'/'+self.cwd+r'/'+file
            return addr
        else: return ''


if __name__ == '__main__':
    fd = ftpDownload(parameter)
    print fd.getFileList()
    #print fd.matchFile()
    #print fd.getAddr()
#!/opt/exptools/bin/python
__author__ = 'sanpingz'

from ftplib import FTP
import re, socket

parameter = {'host':'135.252.226.34',
         'user':'lss',
         'passwd':'lss',
         'cwd':'../../../logs/ctlog',
         'path':'/logs/ctlog',
         'ctid':'10'
}
class ftpDownload:
    def __init__(self,param):
        self.host = param['host']
        self.user = param['user']
        self.passwd = param['passwd']
        self.cwd = param['cwd']
        self.ctid = param['ctid']
        self.path = param.get('path')
    def getFileList(self):
        lt = []
        try:
            ftp = FTP(self.host)
            ftp.login(self.user, self.passwd)
            ftp.cwd(self.cwd)
            ftp.set_pasv(0)
            try:
                lt = ftp.nlst()
            except socket.error:
                #print "port"
                ftp.set_pasv(1)
                lt = ftp.nlst()
        finally:
            ftp.quit()
            ftp.close()
        return lt
    def matchFile(self):
        matched = ''
        num = 0
        try:
            filelist = self.getFileList()
        except Exception: filelist = []
        reg = str(self.ctid)+r'[\.|\,]\d{8}\.\d{4}[\.|\,]ISC\.\w+'
        pattern = re.compile(reg)
        if filelist:
            for file in filelist:
                if pattern.match(file) and int(re.split('[,|.]+',file)[2])>num:
                    matched = file
                    num = int(re.split('[,|.]+',file)[2])
        return  matched
    def getAddr(self, flag='ftp'):
        file = self.matchFile()
        addr = ''
        if file:
            if flag == 'ftp':
                addr = r'ftp://'+self.user+':'+self.passwd+'@'+self.host+r'/'+self.cwd+r'/'+file
            if flag == 'scp':
                addr = self.user+r'@'+self.host+r':'+self.path+r'/'+file
            if flag == 'file':
                addr = self.path+r'/'+file
        return addr


if __name__ == '__main__':
    fd = ftpDownload(parameter)
    print fd.getFileList()
    print fd.matchFile()
    print fd.getAddr()
    print fd.getAddr(flag='file')
    #print fd.matchFile()
    #print fd.getAddr()
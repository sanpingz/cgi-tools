#!/opt/x11r6/bin/python
__author__ = 'sanpingz'

from FTPDownload import ftpDownload
import cgi

print 'Content-type: text/html'
print

param = {'host':'135.2.121.97',
         'user':'lss',
         'passwd':'lss',
         'cwd':'../../../logs/ctlog',
         'ctid':'99'
}
form = cgi.FieldStorage()
p={}
for key in form.keys():
    p[key] = form[key].value
param.update(p)
fd = ftpDownload(param)
print fd.getAddr()
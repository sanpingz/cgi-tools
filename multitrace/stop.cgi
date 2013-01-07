#!/opt/exptools/bin/python
import cgi
from CallTrace import stopCall

print 'Content-type: text/html'
print

form = cgi.FieldStorage()
param = {}
for key in form.keys():
    param[key] = form[key].value
param['labip'] = param.get('labip').split(',')
stop = stopCall(param)
stop.createXML()
stop.startCommand()

print stop.status
#!/opt/x11r6/bin/python
import cgi
from CallTrace import stopCall

print 'Content-type: text/html'
print

form = cgi.FieldStorage()
stop = stopCall(form['labip'].value, form['ctid'].value)
stop.createXML()
stop.startCommand()

print stop.status
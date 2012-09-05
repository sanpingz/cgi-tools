#!/opt/exptools/bin/python
__author__ = 'sanpingz'

import cgi, os

print 'Content-type: text/plain'
print

form = cgi.FieldStorage()
if form.has_key('handle'):
    handle = form['handle'].value
    command = r'/opt/exptools/bin/pq id='+str(handle)
    cb = os.popen(command).read()
    print cb
else: print ''


#!/opt/exptools/bin/python
__author__ = 'sanpingz'

from JsonDB import simpleDB
import cgi
from CallTrace import stopCall

print 'Content-type: text/plain'
print

form = cgi.FieldStorage()
p={}
for key in form.keys():
    p[key] = form[key].value
stop = stopCall(p)
stop.updateData()

handle = form['handle'].value
ctid = form['ctid'].value

db = simpleDB(handle)
user = db.select(ctid)
addr = user.get('addr')

if addr and len(addr)<120:
    print addr
else:
    print ''
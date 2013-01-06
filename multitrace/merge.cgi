#!/opt/exptools/bin/python
import cgi, cgitb
from SimpleFTP import addr

print 'Content-type: text/html'
print

form = cgi.FieldStorage()

res = ''
mid = form.getvalue('mid')
try:
    if mid and isinstance(mid,list):
        res =  addr(mid)
except Exception,e:
    res = ''

print res
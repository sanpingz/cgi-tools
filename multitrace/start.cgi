#!/opt/exptools/bin/python
import cgi, cgitb
import time, re
from CallTrace import startCall, toString

print 'Content-type: text/html'
print

cgitb.enable(display=0, logdir='log')
form = cgi.FieldStorage()

TIMEFORMAT = '%Y-%m-%d %X'
cnt = time.time()+time.altzone+8*3600
curtime = time.strftime(TIMEFORMAT, time.localtime(cnt))

labip = form.getvalue('labip')
ip = []
pm = {}
if labip and isinstance(labip,list):
    reg = '^(?:(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))$'
    for i in labip:
        if i not in ip and re.match(reg,i):
            ip.append(i)
    labip = ip[:]

for key in form.keys():
    pm[key] = form.getvalue(key)

pm['labip'] = labip

start = startCall(pm)
start.createXML()
start.startCommand()

### --thread-- ##
#try:
#    start.startCommand()
#except Exception,e:
#    print "NotCompleted"
#    #print e
#else:
### --thread-- ##

if start.status == 'Failure':
    print "NotCompleted"
else:
    print '<tr id="ct%s">' % start.ctid
    print '<td> <a class="trigger_sb" href="javascript:void(0)">%s</a> </td>' % start.ctid
    print '<td> %s </td>' % start.mode
    if start.mode == 'TELNUM':
        print '<td> %s </td>' % (str(start.callid)+' ('+start.matchdir+')')
    else:
        print '<td> %s </td>' % start.callid
    print '<td> %s </td>' % start.duration
    print '<td class="cb_labip"> %s </td>' % toString(start.labip)
    print '<td class="cb_status"><div> %s </div></td>' % start.status
    print '<td> %s </td>' % curtime
    print '<td class="op_stop">'
    print '<input type="hidden" name="labip" value="%s" />' % toString(start.labip)
    print '<input type="hidden" name="apptype" value="%s" />' % start.apptype
    print '''<input type="hidden" name="ctid" value="%s" />
            <button type="button" class="btn btn-mini ct-button">Stop</button>
            <a class="btn btn-mini btn-success ct-button" style="padding:0; display:none;">Download</a>
            </td>''' % start.ctid
    print '</tr>'

    start.saveData()


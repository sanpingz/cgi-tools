#!/opt/exptools/bin/python
import cgi, cgitb
import time
from CallTrace import startCall

print 'Content-type: text/html'
print

cgitb.enable(display=0, logdir='log')
form = cgi.FieldStorage()
p = {}
for key in form.keys():
    p[key] = form[key].value
start = startCall(p)
start.createXML()

## --thread-- ##
try:
    start.startCommand()
except Exception:
    print "Not completed in given time!"
else:
## --thread-- ##

    TIMEFORMAT = '%Y-%m-%d %X'
    cnt = time.time()+time.altzone+8*3600
    curtime = time.strftime(TIMEFORMAT, time.localtime(cnt))

    print '<tr id="ct%s">' % start.ctid
    print '<td> %s </td>' % start.ctid
    print '<td> %s </td>' % start.mode
    if start.mode == 'TELNUM':
        print '<td> %s </td>' % (str(start.callid)+' ('+start.matchdir+')')
    else:
        print '<td> %s </td>' % start.callid
    print '<td> %s </td>' % start.duration
    print '<td class="cb_labip"> %s </td>' % start.labip
    print '<td class="cb_status"><div> %s </div></td>' % start.status
    print '<td> %s </td>' % curtime
    print '<td class="op_stop">'
    print '<input type="hidden" name="labip" value="%s" />' % start.labip
    print '''<input type="hidden" name="ctid" value="%s" />
        <button type="button" class="btn btn-mini ct-button">Stop</button>
        <a class="btn btn-mini btn-success ct-button" style="padding:0; display:none;">Download</a>
        </td>''' % start.ctid
    print '</tr>'

    start.saveData()

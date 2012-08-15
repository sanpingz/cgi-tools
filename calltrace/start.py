#!/opt/x11r6/bin/python
import cgi
import time
from CallTrace import startCall

print 'Content-type: text/html'
print

form = cgi.FieldStorage()
start = startCall(form['duration'].value, form['mode'].value, form['labip'].value)
start.setCallId(form['callid'].value)
start.createXML()
start.startCommand()

TIMEFORMAT = '%Y-%m-%d %X'
curtime = time.strftime(TIMEFORMAT, time.localtime(time.time()))

print '<tr id="ct%s">' % start.ctid
print '<td> %s </td>' % start.ctid
print '<td> %s </td>' % start.mode
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
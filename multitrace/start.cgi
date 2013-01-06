#!/opt/exptools/bin/python
import cgi, cgitb
import time
from CallTrace import startCall

print 'Content-type: text/html'
print

#cgitb.enable(display=0, logdir='log')
cgitb.enable()
form = cgi.FieldStorage()

TIMEFORMAT = '%Y-%m-%d %X'
cnt = time.time()+time.altzone+8*3600
curtime = time.strftime(TIMEFORMAT, time.localtime(cnt))

def callback(p):
    start = startCall(p)
    start.createXML()

    ## --thread-- ##
    try:
        start.startCommand()
    except Exception,e:
        print "NotCompleted"
        #print e
    else:
    ## --thread-- ##

        print '<tr id="ct%s">' % start.ctid
        print '<td> <a class="trigger_sb" href="javascript:void(0)">%s</a> </td>' % start.ctid
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
        print '<input type="hidden" name="apptype" value="%s" />' % start.apptype
        print '''<input type="hidden" name="ctid" value="%s" />
            <button type="button" class="btn btn-mini ct-button">Stop</button>
            <a class="btn btn-mini btn-success ct-button" style="padding:0; display:none;">Download</a>
            </td>''' % start.ctid
        print '</tr>'

        start.saveData()

pm = {}
labip = form.getvalue('labip')
if isinstance(labip, list):
    for ip in labip:
        pm = {}
        if ip != '':
            for key in form.keys():
                if key != 'labip':
                    pm[key] = form[key].value
                pm['labip']=ip
            callback(pm)
else:
    pm = {}
    for key in form.keys():
        pm[key] = form[key].value
    callback(pm)


#!/opt/exptools/bin/python
import cgi, cgitb
from JsonDB import simpleDB
from CallTrace import toString

print 'Content-type: text/html'
print

cgitb.enable(display=0, logdir='log')

form = cgi.FieldStorage()

def sort_dict(data):
    keys = data.keys()
    try:
        keys = map(int,keys)
    except:pass
    keys.sort()
    keys = map(str,keys)
    return zip(keys, map(data.get, keys))

if form.has_key('handle'):
    handle = form['handle'].value
    db = simpleDB(handle)
    data = db.filter()
    if data:
        data = sort_dict(data)
        for key, value in data:
            print '<tr>'
            print '<td> <a class="trigger_sb" href="javascript:void(0)">%s</a> </td>' % key
            print '<td> %s </td>' % value['mode']
            if value['mode'] == 'TELNUM':
                print '<td> %s </td>' % (value['callid']+' ('+value.get('matchdir')+')')
            else:
                print '<td> %s </td>' % value['callid']
            print '<td> %s </td>' % value['duration']
            print '<td class="cb_labip"> %s </td>' % toString(value['labip'])
            print '<td class="cb_status"><div> %s </div></td>' % value['status']
            print '<td> %s </td>' % value['startime']
            print '<td class="op_stop">'
            print '<input type="hidden" name="labip" value="%s" />' % toString(value['labip'])
            if (value['status'] == 'Stopped') and value.get('addr'):
                print '<input type="hidden" name="ctid" value="%s" />' % key
                print'''<button type="button" class="btn btn-mini ct-button" style="display:none;">Stop</button>
                <a  href="%s" class="btn btn-mini btn-success ct-button" style="padding:0;">Download</a>
                </td>''' % value['addr']
            elif value['status'] == 'Failure':
                print '''<input type="hidden" name="ctid" value="%s" />
                <button type="button" disabled="disabled" class="btn btn-mini ct-button">Stop</button>
                <a class="btn btn-mini btn-success ct-button" style="padding:0; display:none;">Download</a>
                </td>''' % key
            else:
                print '''<input type="hidden" name="ctid" value="%s" />
                <button type="button" class="btn btn-mini ct-button">Stop</button>
                <a class="btn btn-mini btn-success ct-button" style="padding:0; display:none;">Download</a>
                </td>''' % key
            print '</tr>'
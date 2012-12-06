#!/opt/exptools/bin/python
import cgi, os, cgitb
from os.path import join, abspath
__author__ = 'sanpingz'

print 'Content-type: text/plain'
print

cgitb.enable(display=0, logdir='log')
BASE_DIR = abspath('data')
mail = { "calvin":"sanping.zhang@alcatel-lucent.com",
         "david":"david.dn.dong@alcatel-lucent.com",
         "subject":"Call trace feedback"
}
form = cgi.FieldStorage()
handle = form.getvalue('handle')
subject = mail.get('subject')
content = form.getvalue('content')

callback = ''
if handle and subject and content:
    fro = os.popen(r'/opt/exptools/bin/pq -o "%mailto" id='+handle).read()
    if fro:
        fro = '-r '+fro
        fro = fro.replace('\n', '')
    else: fro = ''
    mail_file = join(BASE_DIR, 'mail.temp')
    f = open(mail_file, 'w')
    try:
        f.write(content)
    except Exception:
        pass
    f.close()
    command = 'mailx '+fro+' -s '+'"'+subject+'" '+mail.get('calvin')+','+mail.get('david')+' < '+mail_file
    #command = 'mailx '+fro+' -s '+'"'+subject+'" '+mail.get('calvin')+' < '+mail_file
    callback = os.popen(command).read()
print callback

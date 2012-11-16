#!/opt/exptools/bin/python
__author__ = 'Calvin Zhang(sanping.zhang@alctel-lucent.com)'

import os, cgi, cgitb

print 'Content-type: text/html'
print

cgitb.enable(display=0, logdir='log')
form = cgi.FieldStorage()
cnfgIP = str(form['cnfgIP'].value)
cmdstr = str(form['cmdstr'].value)

cmd = r'./autocmd.exp cnfgIP ' + cnfgIP + ' cmdstr "' + cmdstr + '"'
#print cmd
try:
    result = os.popen(cmd)
    #print result
except Exception, e:
    print e
log = ''
count = 0
while True:
    os.system('sleep 2')
    count += 1
    if os.path.isfile('cmd_result'):
        f = open('cmd_result', 'r')
        try:
            log = f.read()
        finally:
            f.close()
            os.system('rm cmd_result')
        break
    if count >= 10:
        break
if len(log) == 0:
    print 'oops, no logs can be showed'
else:
    print log

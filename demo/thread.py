import   threading, time

TimeoutError = " "

def function(args = [], kwargs = {}):
    z = 1
    if len(args):
        n = args[0]
    else:
        n = 10
    while z < n:
        z += 1
    time.sleep(0.5)
    return z

class FuncWrapper(object):
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.hasReturn = False
    def execute(self):
        self.result = self.func(self.args, self.kwargs)
        self.hasReturn = True

class   Timeout(threading.Thread):
    def __init__(self, timeout, func):
        threading.Thread.__init__(self)
        self.timeout = timeout
        self.func = func
        self.subThread = threading.Thread(target = self.func.execute)
        self.subThread.setDaemon(True)
    def run(self):
        self.subThread.start()
        time.sleep(self.timeout)
        if not self.func.hasReturn:
            raise "TimeoutError"

if   __name__ == "__main__ ":
    func_obj = FuncWrapper(function, [5,], {})
    try :
        t = Timeout(5, func_obj)
        t.run()
        print func_obj.result
    except :
        print "Not completed in given time!"
    func_obj = FuncWrapper(function, [1000,], {})
    try   :
        t = Timeout(5, func_obj)
        t.run()
        print func_obj.result
    except:
        print "Not completed in given time!"
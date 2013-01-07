#!/usr/bin/env python
import threading, time
import os, signal,sys

class FuncWrapper(object):
    def __init__(self, func, args):
        self.func = func
        self.args = args
        self.hasReturn = False

    def execute(self):
        self.result = self.func(self.args)
        self.hasReturn = True


class Timeout(threading.Thread):
    def __init__(self, timeout, func):
        threading.Thread.__init__(self)
        self.timeout = timeout
        self.func = func
        self.subThread = threading.Thread(target=self.func.execute)

    def run(self):
        self.subThread.setDaemon(True)
        self.subThread.start()
        #time.sleep(self.timeout)
        self.subThread.join(timeout=self.timeout)
        if not self.func.hasReturn:
            pid = os.getpid()
            os.kill(pid,signal.SIGTERM)
            raise Exception('TimeoutError')


def function(n=15):
    z = 0
    while z < n:
        z += 1
        print z
        time.sleep(0.5)
    return z

if __name__ == "__main__":
    func_obj = FuncWrapper(function, 15)
    try:
        t = Timeout(3, func_obj)
        t.run()
        print func_obj.result
    except Exception:
        print "Not completed in given time!"

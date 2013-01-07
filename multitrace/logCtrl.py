#!/usr/bin/env python
from os.path import join
import logging, traceback, sys

BASE_DIR = 'data'
LOG_FILE = join(BASE_DIR, 'calltrace.log')

def getLogger(name=None,file='log.log',level=logging.ERROR):
    logger = logging.getLogger(name)
    handler = logging.FileHandler(file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s : %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger

def simpleLog(**args):
    type, value, tb = sys.exc_info()
    fm = traceback.format_exception(type, value, tb)
    logger = getLogger(**args)
    logger.error('%s%s' % (fm[2],fm[1]))

__author__ = 'sanpingz'

import json,pprint

with open('cnfg.json') as f:
    js = json.load(f)
pprint.pprint(js)
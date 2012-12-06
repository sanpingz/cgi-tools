__author__ = 'sanpingz'

def sort_dict(data):
    keys = data.keys()
    keys.sort()
    return zip(keys, map(data.get, keys))

m = { '1': { '1':'a'}, '3': { '3':'b'}, '2': { '2':'c'} }

print sort_dict(m)
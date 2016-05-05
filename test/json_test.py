#!/usr/bin/env python

"""
Assuming this is file mymodule.py, then this string, being the
first statement in the file, will become the "mymodule" module's
docstring when the file is imported.
"""

import json
import dict #It is posible to write all the dictionaries in a different file. to call them just use dict.<name of variable>

#https://docs.python.org/2/library/json.html#json.load

def json_message(x,y):
	z=x.copy()
	z.update(y)
	return json.dumps(z)



json_string = '{"hello":"Nick"}'
parsed_json = json.loads(json_string)
print(parsed_json['hello'])

ip="192.168.2.15"
d = {  #This is a dictionary
    'cmd': 'add_request',
    'ip': "null", #a dictionary can be modified later or directly
    'titles': ['A', 'B','D','C'],
	}
d["ip"]=[ip,"192.168.0.0"] #this is how to assign a variable to a dict field

print(json_message(dict.HEADER,d))

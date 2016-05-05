import NEGRAV

temp = {
	'name': 'temp',
	'units': ['c','F'],
	'resolution': '0.5c',
	'range': ['-25c','75c']
}

mov = {
	'name': 'mov',
	'units': ['NULL'],
	'resolution': 'NULL',
	'range': ['0','1']
}

print("add request:")
print(NEGRAV.add_request("192.168.0.1"))
print("")

print("add response:")
print(NEGRAV.add_response("192.168.0.1"))
print("")

print("node report:")
print(NEGRAV.node_report("192.168.0.5","MN",[temp,mov],[1,2,3]))
print("")

print("get request:")
print(NEGRAV.get_request("array",[1,2,5]))
print("")

print("get response:")
print(NEGRAV.get_response(['5c','20g','35ms']))
print("")

print("alarm report:")
print(NEGRAV.alarm_report("192.168.0.5","temp","35f"))
print("")
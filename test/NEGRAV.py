"""
This file contains all the NEGRAV functions. for all kind of devices
(Base station BS, Mobile node MN and Stationary node SN)
"""

import json

"""List of keys in each cmd type. this is used to verify"""
ADD_REQUEST_keys  = ["source_ip"]
ADD_RESPONSE_keys = ["assign_ip"]
NODE_REPORT_keys  = ["node_ip","type","sensor"]
GET_REQUEST_keys  = ["get_type", "sensor"]
GET_RESPONSE_keys = ["sensor"]
ALARM_REPORT_keys = ["node_ip","sensor","value"]

"""Dictionaries"""
HEADER= { 
	'protocol': 'NEGRAV', 
	'version':'v1.0'
	}

ADD_REQUEST = {
	'cmd': 'add_request',
	'source_ip': 'NULL'
}

ADD_RESPONSE = {
	'cmd': 'add_response',
	'assign_ip': 'NULL'
}

NODE_REPORT = {
	'cmd': 'node_report',
	'node_ip': 'NULL',
	'type': 'NULL',
	'GPS': 'NULL',
	'sensor': 'NULL'
}

GET_REQUEST = {
	'cmd': 'get',
	'get_type': 'NULL',
	'sensor': 'NULL'
}

GET_RESPONSE = {
	'cmd': 'get',
	'sensor': 'NULL'
}

ALARM_REPORT = {
	'cmd': 'alarm_report',
	'node_ip': 'NULL',
	'sensor': 'NULL',
	'value': 'NULL'
}

'''Important Variables'''
IP_BASE = '127.0.0.1'
TCP_PORT_SERVER = 5310
TCP_PORT_CLIENT =5315
BUFFER_SIZE = 1024

NEGRAR_ERROR_NONE 			= 0
NEGRAV_ERROR_INVALID_JSON 	= -1
NEGRAV_ERROR_INVALID_FORMAT = -2



""" send message Functions"""
def json_add_header(header,message):
	aux=header.copy()
	aux.update(message)
	return json.dumps(aux)

def json_add_request(ip):
	aux= ADD_REQUEST.copy()
	aux["source_ip"]=ip
	return json_add_header(HEADER,aux)

def json_add_response(ip):
	aux= ADD_RESPONSE.copy()
	aux["assign_ip"]=ip
	return json_add_header(HEADER,aux)

def json_node_report(ip, type, sensor, GPS):
	aux= NODE_REPORT.copy()
	aux["node_ip"]=ip
	if type in ('MN','SN'):
		aux["type"]=type
	else:
		return "error type"
	aux["sensor"]=sensor
	aux["GPS"]=GPS
	return json_add_header(HEADER,aux)

def json_get_request(get_type, sensor_list):
	aux= GET_REQUEST.copy()
	if get_type in ('all','array'):
		aux["get_type"]=get_type
	else:
		return "error get type"
	aux["sensor"]=sensor_list
	return json_add_header(HEADER,aux)

def json_get_response(sensor_list):
	aux= GET_RESPONSE.copy()
	aux["sensor"]=sensor_list
	return json_add_header(HEADER,aux)

def json_alarm_report(ip, sensor_name, value):
	aux= ALARM_REPORT.copy()
	aux["sensor"]=sensor_name
	aux["value"]=value
	return json_add_header(HEADER,aux)

def negrav_parser(json_msg):
	try:
		parsed = json.loads(json_msg) #Dict that contain the parsed json
	except: 
		print "Invalid Json Format"
		return NEGRAV_ERROR_INVALID_JSON
	try:
		command = parsed['cmd']
	except:
		print "Invalid NEGRAV message. Missing cmd"
		return NEGRAV_ERROR_INVALID_FORMAT
	try:
		if command == "add_response":
			for key in ADD_RESPONSE_keys:
				parsed[key]
		elif command == "add_request":
			for key in ADD_REQUEST_keys:
				parsed[key]
		elif command == "node_report":
			for key in NODE_REPORT_keys:
				parsed[key]
		elif command == "get":
			pass
		elif command == "alarm_report":
			for key in ALARM_REPORT_keys:
				parsed[key]
			pass
		else:
			print "Command Not found"
			return NEGRAV_ERROR_INVALID_FORMAT 
	except:
		print 'Invalid NEGRAV message. Missing "%s"' % key
		return NEGRAV_ERROR_INVALID_FORMAT

	return (NEGRAR_ERROR_NONE, parsed)

(status, parsed) = negrav_parser('{"protocol": "NEGRAV","version":"v1.0","cmd":"add_response","assign_ip":"0.0.0.0"}')
print parsed["cmd"]

"""
This file contains all the NEGRAV functions. for all kind of devices
(Base station BS, Mobile node MN and Stationary node SN)
"""

import json

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

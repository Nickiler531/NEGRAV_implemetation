"""
This file contains all the NEGRAV functions. for all kind of devices
(Base station BS, Mobile node MN and Stationary node SN)
"""

import json
import socket

"""List of keys in each cmd type. this is used to verify"""
ADD_REQUEST_keys  = ["source_ip"]
ADD_RESPONSE_keys = ["assign_ip"]
NODE_REPORT_keys  = ["node_ip","type","sensor"]
GET_REQUEST_keys  = ["get_type", "sensor"]
GET_RESPONSE_keys = ["sensor"]
ALARM_REPORT_keys = ["node_ip","sensor","value"]
MOVE_REQUEST_keys = ["target_location"]

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

CONFIGURE_REQUEST = {
	'cmd': 'node_configure',
	'assign_ip': 'NULL',
	'set_node_time': 'NULL',
	'sensor': 'NULL'
}

MOVE_REQUEST ={
	'cmd':'move_request',
	'target_location':'NULL',
	'road_map':'NULL'
}

'''Important Variables'''
IP_BASE = '10.0.0.100'
TCP_PORT_SERVER = 5310
TCP_PORT_CLIENT =5315
BUFFER_SIZE = 1024

NEGRAR_ERROR_NONE 			= 0
NEGRAV_ERROR_INVALID_JSON 	= -1
NEGRAV_ERROR_INVALID_FORMAT = -2



"""-------------------BASIC JSON FUNCTIONS-------------------------"""

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
	aux["node_ip"]=ip
	aux["sensor"]=sensor_name
	aux["value"]=value
	return json_add_header(HEADER,aux)

def json_config_request (ip, node_time, sensor):
	aux = CONFIGURE_REQUEST.copy()
	aux["assign_ip"]=ip
	aux["set_node_time"]=node_time
	aux["sensor"]=sensor
	return json_add_header(HEADER,aux)

def json_move_request (target_location,road_map):
	aux = MOVE_REQUEST.copy()	
	aux["target_location"]=target_location
	aux["road_map"]=road_map
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
		elif command == "node_configure":
			pass
		elif command == "move_request":
			for key in MOVE_REQUEST_keys:
				parsed[key]
		else:
			print "Command Not found"
			return NEGRAV_ERROR_INVALID_FORMAT 
	except:
		print 'Invalid NEGRAV message. Missing "%s"' % key
		return NEGRAV_ERROR_INVALID_FORMAT

	return (NEGRAR_ERROR_NONE, parsed)

(status, parsed) = negrav_parser('{"protocol": "NEGRAV","version":"v1.0","cmd":"add_response","assign_ip":"0.0.0.0"}')
print parsed["cmd"]


def server_init():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('',TCP_PORT_SERVER))
	s.listen(1)
	return s

def server_listening(s):
	conn, address = s.accept()
	error, data = negrav_parser(conn.recv (BUFFER_SIZE))
	return conn, address, error, data

"""-------------------------------------------Base Station Functions----------------------------------------------------"""

def add_response (conn,ip):
	conn.sendall(json_add_response(ip))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	#print json_add_response (ip)
	#conn.close()
	
def get_request(ip, get_type = "all", sensor_list = []):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, TCP_PORT_SERVER))
	s.sendall(json_get_request (get_type, sensor_list))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	error, data = negrav_parser(s.recv(BUFFER_SIZE))
	s.close()
   	return error, data

def config_request(ip,assign_ip = '0', node_time = '0', sensor = '0'):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, TCP_PORT_SERVER))
	s.sendall(json_config_request(assign_ip, node_time, sensor))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	#MIRAR SI SE PUEDE COLOCAR UN TCP ACK
	s.close()


def move_request(ip, target_location, road_map = '0'):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((ip, TCP_PORT_SERVER))
	s.sendall(json_move_request(target_location, road_map))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	#MIRAR SI SE PUEDE COLOCAR UN TCP ACK
	s.close()

"""------------------------------------------------Node Station Functions----------------------------------------------"""

def add_request(ip):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IP_BASE, TCP_PORT_SERVER))
	s.sendall(json_add_request(ip))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	error,data = negrav_parser(s.recv(BUFFER_SIZE))
	s.close()
   	return error,data

def node_report(ip, type, sensor, GPS):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IP_BASE, TCP_PORT_SERVER))
	s.sendall(json_node_report(ip, type, sensor, GPS))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	s.close()

def get_response(conn, get_type, sensor_list, sensor_values):
	if get_type == 'all':
		sensor_list = sensor_values
	else:
		i=0

		while i < len(sensor_list):
			aux = sensor_list[i]
			if aux == 'battery':
				sensor_list[i] = sensor_values [0]
			#Estoy suponiendo que los valores estan en una lista ordenada
			if aux == 'temp':
				#print sensor_list
				sensor_list[i] = sensor_values [1]
				#print sensor_list
			if aux == 'radiation':
				sensor_list[i] = sensor_values [2]
			if aux == 'humidity':
				sensor_list[i] = sensor_values [3]
			if aux == 'extra_1':
				sensor_list[i] = sensor_values [4]
			if aux == 'extra_2':
				sensor_list[i] = sensor_values [5]
			i = i+1
		
	conn.sendall(json_get_response(sensor_list))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent

def alarm_report(ip, sensor_name, value):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IP_BASE, TCP_PORT_SERVER))
	s.sendall(json_alarm_report(ip, sensor_name, value))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	#MIRAR SI SE PUEDE COLOCAR UN TCP ACK
	#error,data = negrav_parser(s.recv(BUFFER_SIZE))
	s.close()
   	#return data
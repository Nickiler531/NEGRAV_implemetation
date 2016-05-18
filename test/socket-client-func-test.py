#!/usr/bin/env python

import time
import socket
from NEGRAV import *

IP_BASE = '127.0.0.1'

def add_request(ip):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.bind(('',TCP_PORT_CLIENT))
	s.connect((IP_BASE, TCP_PORT_SERVER))
	#print json_add_request(ip)
	s.sendall(json_add_request(ip))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	#print json_add_request(ip)
	data = s.recv(BUFFER_SIZE)
	# ACA VA EL PARSER
	#print 'Received', data
	#s.send("{testing 123 ACK!!!!}")
 	s.close()
   	return data

def node_report(ip, type, sensor, GPS):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IP_BASE, TCP_PORT_SERVER))
	s.sendall(json_node_report(ip, type, sensor, GPS))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	s.close()

def server_listening():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('',TCP_PORT_SERVER))
	s.listen(1)
	conn, address = s.accept()
	#while 1:
	data = conn.recv (BUFFER_SIZE)
		#Aca va el parser?
	#	if not data: break
	#print data
	return conn, address, data

def get_response(conn, get_type, sensor_list, sensor_values):
	if get_type == 'all':
		sensor_list = sensor_values
	else:
		i=0
		sensor_quantity = len(sensor_list)
		while i < sensor_quantity:
			aux = sensor_list[i]
			if aux == 'battery':
				sensor_list[i] = sensor_values [0]
			#Estoy suponiendo que retorno una lista ordenada de valores para interpretarlos facilmente en la BS
			if aux == 'temp':
				sensor_list[i] = sensor_values [1]
			if aux == 'radiation':
				sensor_list[i] = sensor_values [2]
			if aux == 'humidity':
				sensor_list[i] = sensor_values [3]
			if aux == 'extra_1':
				sensor_list[i] = sensor_values [4]
			if aux == 'extra_2':
				sensor_list[i] = sensor_values [5]
			i = i+1
		#if 'temp'in sensor_list:
		#	sensor_list [1] = sensor_values [1]
		#else:
		#	sensor_list [1] = 0
		
		#if 'radiation'in sensor_list:
		#	sensor_list [2] = sensor_values [2]
		#else:
		#	sensor_list [2] = 0

		#if 'humidity'in sensor_list:
		#	sensor_list [3] = sensor_values [3]
		#else:
		#	sensor_list [3] = 0

		#if 'extra_1'in sensor_list:
		#	sensor_list [4] = sensor_values [4]
		#else:
		#	sensor_list [4] = 0

		#if 'extra_2'in sensor_list:
		#	sensor_list [5] = sensor_values [5]
		#else:
		#	sensor_list [5] = 0
	conn.sendall(json_get_response(sensor_list))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent




		 
   
data = add_request('10.0.2.1')

print 'Received add response:', data

ip = data[15]+data[16]+data[17]+data[18]+data[19]+data[20]+data[21]+data[22] #no pude leerlo usando ip=data["assign_ip"]
print 'new ip:', ip

node_report (ip,'SN','temp',('3.53N','6.54E'))# revisar como se envian las coordenadas, aca solo me acepto un entero
time.sleep(5)
conn, adress, data = server_listening()
print 'received get request', data

get_response(conn,'array',['battery', 'temp','humidity'], [5,37,10,30,1,2])


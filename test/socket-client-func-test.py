#!/usr/bin/env python

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
   
data = add_request('10.0.2.1')

print 'Received add response:', data

ip = data[15]+data[16]+data[17]+data[18]+data[19]+data[20]+data[21]+data[22] #no pude leerlo usando ip=data["assign_ip"]
print 'new ip:', ip

node_report (ip,'SN','temp','3')# revisar como se envian las coordenadas, aca solo me acepto un entero

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind(('',TCP_PORT_CLIENT))
#s.connect((IP_BASE, TCP_PORT_SERVER))
#s.sendall(json_add_request('192.168.1.102'))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	
#data = s.recv(BUFFER_SIZE)
# ACA VA EL PARSER
#s.close()
#print 'Received', repr(data)
#TCP_IP = '127.0.0.1'
#TCP_PORT = 5310
#TCP_PORT_SEND=5315
#BUFFER_SIZE = 1024

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind(('',TCP_PORT_CLIENT))
#s.connect((IP_BASE, TCP_PORT_SERVER))

#s.sendall("{testing 123}")
#data = s.recv(BUFFER_SIZE)
#print "received data:", data
#s.send("{testing 123 ACK!!!!}")
#s.close()

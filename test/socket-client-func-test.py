#!/usr/bin/env python

import socket
from NEGRAV import *

def add_request(ip):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('',TCP_PORT_CLIENT))
	s.connect((IP_BASE, TCP_PORT_SERVER))
	s.sendall("hola")#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	
	data = s.recv(BUFFER_SIZE)
   # ACA VA EL PARSER
   s.close()
   
add_request ('')

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

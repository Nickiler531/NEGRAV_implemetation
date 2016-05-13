import socket
from NEGRAV import *

def add_request(ip):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IP_BASE, TCP_PORT_SERVER))
	s.sendall(json_add_request(ip))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	data = s.recv(BUFFER_SIZE)
   	s.close()
   	return data

def server_listening():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('',TCP_PORT_SERVER))
	s.listen(1)
	conn, address = s.accept()
	data = conn.recv (BUFFER_SIZE)
	#Aca va el parser?
	return conn, address, data

def add_response (conn,ip):
	conn.sendall(json_add_response(ip))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	#conn.close() the client does this

def node_report(ip, type, sensor, GPS):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IP_BASE, TCP_PORT_SERVER))
	s.sendall(json_node_report(ip, type, sensor, GPS))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	s.close()
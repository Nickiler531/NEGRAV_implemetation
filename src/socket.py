import socket
from NEGRAV import *

def add_request(ip):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('',TCP_PORT_CLIENT))
	s.connect((IP_BASE, TCP_PORT_SERVER))
	s.sendall(json_add_request(ip))#On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent
	
	data = s.recv(BUFFER_SIZE)
   # ACA VA EL PARSER
   s.close()




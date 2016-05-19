#!/usr/bin/env python

import time
import socket
from NEGRAV import *

#TCP_IP = ''
#TCP_PORT = 5310
#BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((TCP_IP, TCP_PORT))
#s.listen(1)

#conn, addr = s.accept()
#print 'Connection address:', addr
#while 1:
 #   data = conn.recv(BUFFER_SIZE)
 #   if not data: break
  #  print "received data:", data
   # conn.send("{testing 123 ack?}")
    #data = conn.recv(BUFFER_SIZE)
    #print "received data:", data
#conn.close()





def server_listening():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('',TCP_PORT_SERVER))
	s.listen(1)
	conn, address = s.accept()
	error, data = negrav_parser(conn.recv (BUFFER_SIZE))
	return conn, address, error, data

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

conn, adress, error, data = server_listening()
print "received add request:", data
print 'Error:', error
add_response(conn, '10.0.0.3')
conn, adress, error, data = server_listening()
print "received node report:", data
print 'Error:', error
aux = data["sensor"]
print "!!!!!!!!!!%r" % aux

sensor_list = []
print len(aux)
i = 0
while i < len(aux):
	sensor_list.append(aux[i]['name'])
	i += 1
print sensor_list
time.sleep(5)

error, data = get_request (IP_BASE,'array',sensor_list)
print "received get response", data
print 'Error:', error
#!/usr/bin/env python

import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5310
TCP_PORT_SEND=5315
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',TCP_PORT_SEND))
s.connect((TCP_IP, TCP_PORT))

s.sendall("{testing 123}")
data = s.recv(BUFFER_SIZE)
print "received data:", data
s.send("{testing 123 ACK!!!!}")

s.close()

#!/usr/bin/env python

import time
import socket
from NEGRAV import *

IP_BASE = '127.0.0.1'

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

def server_listening():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('',TCP_PORT_SERVER))
	s.listen(1)
	conn, address = s.accept()
	error, data = negrav_parser(conn.recv (BUFFER_SIZE))
	return conn, address, error, data

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

MIN_DELTA = 5


def move_update (conn, target_location, location, delta, battery, range_status, current_target = '0'):
	
	if delta < MIN_DELTA:
		reason = "no_movement"
	elif range_status == "bad":
		reason = "out_of_range"
	elif target_location == location: #probablemente sera necesario utilizar una tolerancia
		reason = "destination_reached"
	else:
		reason = 'moving'
	print reason
	conn.sendall(json_move_update(location,str(delta), battery, current_target))
	return reason

def move_done(conn, location, reason, battery):
	conn.sendall(json_move_done(location, reason, battery))



		 
   
error, data = add_request('10.0.2.1')
print 'Received add response:', data
print 'Error:', error

ip=data["assign_ip"]
print 'new ip:', ip

node_report (ip,'SN',[{'name':'temp',"units":['C','F']} , {'name':'humidity',"units":['HR','%']} ],('3.53N','6.54E'))# revisar como se envian las coordenadas, aca solo me acepto un entero

time.sleep(5)

conn, adress, error, data = server_listening()
print 'received get request', data
print 'Error:', error
get_type = data ["get_type"]
sensor_list = data["sensor"]
sensor_values = [5,37,10,30,1,2]
get_response(conn,get_type,sensor_list, sensor_values)

time.sleep (5)

sensor_list = data["sensor"]
#print aux
#sensor_list = []

#i = 0
#while i < len(aux):
#	sensor_list.append(aux[i]['name'])
#	i += 1

#print sensor_list
for name in sensor_list :
	#print name
	if name == 'battery' and sensor_values[0]>4:
		alarm_report ('10.0.0.3', 'battery', sensor_values[0])
	if name == 'temp' and sensor_values[1]>35:
		alarm_report ('10.0.0.3', 'temp', sensor_values[1])
	if name == 'radiation' and sensor_values[2]>9:
		alarm_report ('10.0.0.3', 'radiation', sensor_values[2])
	if name == 'humidity' and sensor_values[3]>20:
		alarm_report ('10.0.0.3', 'humidity', sensor_values[3])
	if name == 'extra_1' and sensor_values[4]>35:
		alarm_report ('10.0.0.3', 'extra_1', sensor_values[4])
	if name == 'extra_2' and sensor_values[5]>35:
		alarm_report ('10.0.0.3', 'extra_2', sensor_values[5])
	time.sleep (1)
	#pass



conn, adress, error, data = server_listening()
print 'received configure request:', data
print 'Error:', error

if data["assign_ip"] != '0':
	ip = data["assign_ip"]
	print "new ip:", ip
if data["set_node_time"] != '0':
	node_time = data["set_node_time"]
	print "new node time:"
if data["sensor"] != '0':
	aux = data["sensor"]
	sensor_list = []
	i = 0
	while i < len(aux):

		if aux[i]['name'] == 'temp':
			temp_period = aux[i]['period']
			temp_h_alarm =  aux[i]['alarms'][0]
			temp_l_alarm =  aux[i]['alarms'][1]
			print "new temp period:", temp_period
			print "new hi alarm:", temp_h_alarm
			print "new low alarm", temp_l_alarm

		if aux[i]['name'] == 'radiation':
			radiation_period = aux[i]['period']
			radiation_h_alarm =  aux[i]['alarms'][0]
			radiation_l_alarm =  aux[i]['alarms'][1]
			print "new radiation period:", radiation_period
			print "new hi alarm:", radiation_h_alarm
			print "new low alarm", radiation_l_alarm

		if aux[i]['name'] == 'humidity':
			humidity_period = aux[i]['period']
			humidity_h_alarm =  aux[i]['alarms'][0]
			humidity_l_alarm =  aux[i]['alarms'][1]
			print "new humidity period:", humidity_period
			print "new hi alarm:", humidity_h_alarm
			print "new low alarm", humidity_l_alarm

		if aux[i]['name'] == 'extra_1':
			extra_1_period = aux[i]['period']
			extra_1_h_alarm =  aux[i]['alarms'][0]
			extra_1_l_alarm =  aux[i]['alarms'][1]
			print "new extra_1 period:", extra_1_period
			print "new hi alarm:", extra_1_h_alarm
			print "new low alarm", extra_1_l_alarm

		if aux[i]['name'] == 'extra_2':
			extra_2_period = aux[i]['period']
			extra_2_h_alarm =  aux[i]['alarms'][0]
			extra_2_l_alarm =  aux[i]['alarms'][1]
			print "new extra_2 period:", extra_2_period
			print "new hi alarm:", extra_2_h_alarm
			print "new low alarm", extra_2_l_alarm
		i += 1

time.sleep(5)

conn, adress, error, data = server_listening()
print 'received move request:', data
print 'Error:', error

move_target_lat = data['target_location'][0]
move_target_long = data['target_location'][1]

if data['road_map'] != '0':
	road_map = data['road_map']
#else algoritmo de ruta

print "move target lat and long:", move_target_lat,move_target_long
print "road_map:", road_map

location = ['0','0']
target_location = data["target_location"]
i=0;
aux = 1
while aux == 1:
	i+=1			# en esta linea va la funcion de movimiento se deben actualizar aca los valores que se le pasan a move_update
					# se debe actualizar tambien el current target
	if i>3:			# con i estoy simulando la funcion de movimiento del nodo
		location = target_location
	reason = move_update (conn, target_location, location, 10, '5', 'good', '12')
	if reason != 'moving':
		aux = 0
	time.sleep(1)	#aca iria el periodo para realizar las actualizaciones de move
battery = '5'
move_done(conn, location, reason, battery)

	



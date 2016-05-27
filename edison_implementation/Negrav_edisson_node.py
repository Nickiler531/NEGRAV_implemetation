import random
import pickle
import time
import os
import sys
import errno
import pyupm_grove as grove

sys.path.append("/opt/NEGRAV/src")
from NEGRAV import *

NODE_CONFIG = "/opt/NEGRAV/node.config"

#Button init constants
BUTTON = "44"
GPIO_ADDRESS = "/sys/class/gpio/gpio%s" % BUTTON
DIRECTION_ADDRESS = "%s/direction" % GPIO_ADDRESS
VALUE_ADDRESS = 	"%s/value" % GPIO_ADDRESS
EXPORT_ADDRESS = 	"/sys/class/gpio/export"

#Stationary node Ip pool 10.1.0.1 - 10.1.10.255 (assigned by the base Station)
#stationary node momentary IP pool 10.1.100.1 - 10.1.100.100 (Randomly selected)

#Mobile node Ip pool 10.2.0.1 - 10.2.10.255 (assigned by the base Station)
#Mobile node momentary IP pool 10.2.100.1 - 10.2.100.100 (Randomly selected)


def assign_momentary_ip(node_type):
	'''Returns a random ip depending on the type of node'''
	aux_random = random.randint(1,100)
	if node_type == "MN":
		return "10.2.100." + str(aux_random)
	elif node_type == "SN":
		return "10.1.100." + str(aux_random)
	else:
		print "Fatal Error: Unrecognized node type"
		os.exit()

def read_SSID():
	'''Read the dipswitch/config file or thing that set the SSID and return the complete SSID'''
	return "NEGRAV-1"

def wait_for_add_process():
	button = grove.GroveButton(0)
	print ""
	print ""
	time.sleep(1)
	print "Press The button to add the node to the network"
	while button.value() == 0:
		time.sleep(1)
	print "Add process in progress!!! please wait"

def init_env():
	try:
		f = open(NODE_CONFIG)
		info_pickle, sensor_pickle, alarm_pickle = pickle.load(f)
		f.close()
		return info_pickle, sensor_pickle, alarm_pickle
	except:
		print "Fatal Error: Base Files do not exist or are corrupted. Deploy them again"
		sys.exit()

def save_env(info_pickle):
	try:
		f = open(NODE_CONFIG, 'w')
		pickle.dump(info_pickle, f)
		f.close()
	except:
		print "FATAL ERROR: Could not save de enviroment"
		sys.exit()



#Program Start. Load node information
node_info, sensor_value, sensor_alarm  = init_env()
ssid = read_SSID()
add_process = False

#check if the node have an assigned IP or have to be added to a network
if node_info["node_ip"] == "NULL":
	ip = assign_momentary_ip(node_info["type"])
	add_process = True

	print "\n\n\n\n\n\n"
	print "Welcome to the set up of the node."
	print "This node have a momentary ip: %s" % ip
else:
	ip = node_info["node_ip"]
	print "\n\n\n\n\n\n"
	print "Ip found. Stored IP is %s" % ip

	
print "The current NEGRAV network is = '%s'" % ssid
print "Setting the wifi ad-hoc network"
os.system("sh /opt/NEGRAV/wifi_adhoc_setup.sh %s" % ssid)
time.sleep(5)
os.system("ifconfig wlan0 %s" % ip)
time.sleep(1)
os.system("ifconfig wlan0")

while add_process:
	wait_for_add_process()
	error, json_data = add_request(ip)
	if not error:
		print 'Received add response:', json_data
		ip = json_data["assign_ip"]
		print 'new ip:', ip
		time.sleep(3)
		os.system("ifconfig wlan0 %s" % ip)
		os.system("ifconfig wlan0")
		node_info["node_ip"] = ip;
		save_env((node_info, sensor_value, sensor_alarm))
		node_report(ip, node_info["type"], node_info["sensor"])
		add_process = False


#Server listening
ss = server_init()
while 1:
	
	conn, adress, error, data = server_listening(ss)
	if data["cmd"] == "get":
		print "\n", "-" * 15, "GET REQUEST RECEIVED", "-" * 15
		print "received get request:", data
		if data["get_type"] != 'all':
			get_response(conn, sensor_value, data["type"],data["sensor"])
		else:
			get_response(conn, sensor_value)
	
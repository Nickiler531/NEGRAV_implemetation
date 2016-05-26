import random
import pickle
import time
import os
import sys

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
	if not os.path.exists(GPIO_ADDRESS):
		os.system("echo %s > %s" % (BUTTON, EXPORT_ADDRESS))
		os.system("echo in > %s" % DIRECTION_ADDRESS)
	f = open(VALUE_ADDRESS,'r')
	a = int(f.read())
	print ""
	print ""
	print "Press The button to add the node to the network"
	while a == 1:
		time.sleep(1)
		f.seek(0)
		a = int(f.read())
	f.close()
	print "Add process in progress!!! please wait"


#Program Start. Load node information
try:
	f = open(NODE_CONFIG)
	node_info = pickle.load(f)
	f.close()
except:
	print "Fatal Error: Base Files do not exist or are corrupted. Deploy them again"
	sys.exit()

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
time.sleep(2)
os.system("ifconfig wlan0 %s" % ip)
time.sleep(2)

if add_process:
	wait_for_add_process()
	error, data = add_request(ip)
	print 'Received add response:', data
	print 'Error:', error
	ip = data["assign_ip"]
	print 'new ip:', ip
	node_report (ip,'SN',[{'name':'temp',"units":['C','F']} , {'name':'humidity',"units":['HR','%']} ],('3.53N','6.54E'))# revisar como se envian las coordenadas, aca solo me acepto un entero




import pickle
import time
import os
import sys
import re

sys.path.append("/opt/NEGRAV/src")
from NEGRAV import *

NODE_DB = "/opt/NEGRAV/node.db" #database of all the nodes in the network

IP_BASE_STATION = "10.0.0.100"

#Stationary node Ip pool 10.1.0.1 - 10.1.10.255 (assigned by the base Station)
#stationary node momentary IP pool 10.1.100.1 - 10.1.100.100 (Randomly selected)

#Mobile node Ip pool 10.2.0.1 - 10.2.10.255 (assigned by the base Station)
#Mobile node momentary IP pool 10.2.100.1 - 10.2.100.100 (Randomly selected)


# def assign_momentary_ip(node_type):
# 	'''Returns a random ip depending on the type of node'''
# 	aux_random = random.randint(1,100)
# 	if node_type == "MN":
# 		return "10.2.100." + str(aux_random)
# 	elif node_type == "SN":
# 		return "10.1.100." + str(aux_random)
# 	else:
# 		print "Fatal Error: Unrecognized node type"
# 		os.exit()

def read_SSID():
	'''Read the dipswitch/config file or thing that set the SSID and return the complete SSID'''
	return "NEGRAV-1"

def get_avaiable_ip(temporary_ip):
	'''Used in add process. sees if the ip is valid and return the next avaiable one for the corresponding node'''
	SN = re.compile("10.1.100.[1-99]")
	MN = re.compile("10.2.100.[1-99]")
	if SN.match(temporary_ip):
		return '10.1.0.50'
	elif MN.match(temporary_ip):
		return '10.2.0.50'
	else:
		print "Fatal Error: Base Files do not exist or are corrupted. Deploy them again"
		sys.exit()

#Program Start. Load node information
try:
	f = open(NODE_DB)
	node_db = pickle.load(f)
	f.close()
except:
	print "Fatal Error: Base Files do not exist or are corrupted. Deploy them again"
	sys.exit()

ssid = read_SSID()


print "\n\n\n\n\n\n"
print "Welcome to the NEGRAV Base Station"
print "The current NEGRAV network is = '%s'" % ssid
print 'Ip fused will be the default: "%s" ' % IP_BASE_STATION
print "Setting the wifi ad-hoc network"
os.system("sh /opt/NEGRAV/wifi_adhoc_setup.sh %s" % ssid)
time.sleep(2)
os.system("ifconfig wlan0 %s" % IP_BASE_STATION)
time.sleep(2)




#Server listening
ss = server_init()
while 1:
	
	conn, adress, error, data = server_listening(ss)
	if data["cmd"] == "add_request":
		print "received add request:", data
		print 'Error:', error
		print data["source_ip"]
		add_response(conn,get_avaiable_ip(data["source_ip"]))
		conn, adress, error, data = server_listening(ss)
		print "received node report:", data
		print 'Error:', error
		aux = data["sensor"]
		print aux#"!!!!!!!!!!%r" % aux





import pickle
import time
import os
import sys
import re
import thread

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

def init_env():
	try:
		f = open(NODE_DB)
		info_pickle = pickle.load(f)
		f.close()
		return info_pickle
	except:
		print "Fatal Error: Base Files do not exist or are corrupted. Deploy them again"
		sys.exit()

def save_env(info_pickle):
	try:
		f = open(NODE_DB, 'w')
		pickle.dump(info_pickle, f)
		f.close()
	except:
		print "FATAL ERROR: Could not save de enviroment"
		sys.exit()


def test_me():
	while 1:
		print "HELLOOO"
		time.sleep(1)


#Program Start. Load node information
node_db = init_env()
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


thread.start_new_thread(test_me,())

#Server listening
ss = server_init()
while 1:
	
	conn, adress, error, data = server_listening(ss)
	if data["cmd"] == "add_request":
		print "\n", "-" * 15, "ADD REQUEST RECEIVED", "-" * 15
		print "received add request:", data
		print data["source_ip"]
		temporary_ip = get_avaiable_ip(data["source_ip"])
		add_response(conn, temporary_ip)
		conn, adress, error, data = server_listening(ss)
		print "received node report:", data
		node_db.append(data)
		save_env(node_db)
	elif data["cmd"] == "alarm_report":
		print "\n", "-" * 15, "ALARM REPORT RECEIVED", "-" * 15
	else:
		print "\n", "-" * 15, "UNKNOWN CMD RECEIVED", "-" * 15

		





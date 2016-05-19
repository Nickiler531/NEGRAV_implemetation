import random
import pickle

NODE_CONFIG = "/opt/NEGRAV/node.config"

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



#Program Start. Load node information
try:
	f = open(NODE_CONFIG)
	node_info = pickle.load(f)
	f.close()
except:
	print "Fatal Error: Base Files do not exist or are corrupted. Deploy them again"
	os.exit()

ssid = read_SSID()

#check if the node have an assigned IP or have to be added to a network
if node_info["node_ip"] == "NULL":
	new_ip = assign_momentary_ip(node_info["type"])
	
	print "\n\n\n\n\n\n"
	print "Welcome to the set up of the node."
	print "This node have a momentary ip: %s" % new_ip
	print "The current NEGRAV network is = '%s'" % ssid
	print "Setting the wifi ad-hoc network"
	os.system("sh /opt/NEGRAV/wifi_adhoc_setup.sh %s" % ssid)


	os.system("ifconfig wlan0 %s" % new_ip)




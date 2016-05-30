import random
import pickle
import time
import os
import sys
import errno
import pynmea2
import threading
import signal
import math

sys.path.append("/opt/NEGRAV/src")
from NEGRAV import *

NODE_CONFIG = "/opt/NEGRAV/node.config"

#Button init constants
BUTTON = "44"
GPIO_ADDRESS = "/sys/class/gpio/gpio%s" % BUTTON
DIRECTION_ADDRESS = "%s/direction" % GPIO_ADDRESS
VALUE_ADDRESS = 	"%s/value" % GPIO_ADDRESS
EXPORT_ADDRESS = 	"/sys/class/gpio/export"

GPS_ON = "46"
GPS_ADDRESS = "/sys/class/gpio/gpio%s" % GPS_ON
GPS_DIRECTION_ADDRESS = "%s/direction" % GPS_ADDRESS
GPS_VALUE_ADDRESS =         "%s/value" % GPS_ADDRESS


statusLock = threading.Lock()


#Stationary node Ip pool 10.1.0.1 - 10.1.10.255 (assigned by the base Station)
#stationary node momentary IP pool 10.1.100.1 - 10.1.100.100 (Randomly selected)

#Mobile node Ip pool 10.2.0.1 - 10.2.10.255 (assigned by the base Station)
#Mobile node momentary IP pool 10.2.100.1 - 10.2.100.100 (Randomly selected)

def signal_handler(signal, frame):
        print "\n", "-" * 15, "CTRL + C RECEIVED", "-" * 15
        get_cycle.stop()
        sys.exit(0)

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
	time.sleep(1)
	print "Press The button to add the node to the network"
	while a == 1:
		time.sleep(1)
		f.seek(0)
		a = int(f.read())
	f.close()
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

class getCycle (threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
		os.system("stty -F /dev/ttyMFD1 4800")
		if not os.path.exists(GPS_ADDRESS):
			os.system("echo %s > %s" % (GPS_ON, EXPORT_ADDRESS))
	                os.system("echo out > %s" % GPS_DIRECTION_ADDRESS)
		
		os.system("echo 1 > %s" % GPS_VALUE_ADDRESS)
		time.sleep(1)
                os.system("echo 0 > %s" % GPS_VALUE_ADDRESS)
		self._run = True
        def stop(self):
		#To turn off GPS
		os.system("echo 1 > %s" % GPS_VALUE_ADDRESS)
                time.sleep(1)
                os.system("echo 0 > %s" % GPS_VALUE_ADDRESS)
                self._run = False
		self.f.close()
        def run(self):
                print "\n", "-" * 15, "STARTING THREAD", "-" * 15
                f = open("/dev/ttyMFD1")
		streamreader = pynmea2.NMEAStreamReader(f)
		a = 0
		while self._run:
			try:
				print "trying"
				msg = streamreader.next()
				Lat = int(msg.lat[:2]) + float(msg.lat[2:])/60    
				Lon = int(msg.lon[:3]) + float(msg.lon[3:])/60
				print Lat, Lon
				print "%.4f%s,%.4f%s vs %s%s, %s%s" % (Lat, msg.lat_dir, Lon, msg.lon_dir, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir)
				statusLock.acquire(1)
				sensor_value["GPS"] = "%.4f%s,%.4f%s" % (Lat, msg.lat_dir, Lon, msg.lon_dir)
				statusLock.release()
			except:			
				pass
			statusLock.acquire(1)
			sensor_value["random"] = str(random.randint(1,100))
			sensor_value["sin"] = math.sin(a)
			a += 0.1
			statusLock.release()
			print "\n", "-" * 15, "SENSORS UPDATED", "-" * 15
			print sensor_value
                f.close()
		return



#Program Start. Load node information
signal.signal(signal.SIGINT, signal_handler)
node_info, sensor_value, sensor_alarm  = init_env()
ssid = read_SSID()
add_process = False

get_cycle = getCycle()

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

get_cycle.start()

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
	

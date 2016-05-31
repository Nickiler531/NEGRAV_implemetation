import random
import pickle
import time
import os
import sys
import errno
import signal
import threading
import pyupm_grove as grove
import pyupm_mma7660 as upmMMA7660

sys.path.append("/opt/NEGRAV/src")
from NEGRAV import *

NODE_CONFIG = "/opt/NEGRAV/node.config"

#Button init constants
#BUTTON = "44"
TEMP_PIN = 0
LIGHT_PIN = 1
#Accelerometer init


#GPIO_ADDRESS = "/sys/class/gpio/gpio%s" % BUTTON
#DIRECTION_ADDRESS = "%s/direction" % GPIO_ADDRESS
#VALUE_ADDRESS = 	"%s/value" % GPIO_ADDRESS
#EXPORT_ADDRESS = 	"/sys/class/gpio/export"

statusLock = threading.Lock()

temp = grove.GroveTemp(TEMP_PIN)
light = grove.GroveLight(LIGHT_PIN)
# Instantiate an MMA7660 on I2C bus 0
myDigitalAccelerometer = upmMMA7660.MMA7660(
           	upmMMA7660.MMA7660_I2C_BUS,
            upmMMA7660.MMA7660_DEFAULT_I2C_ADDR);

ax = upmMMA7660.new_floatp()
ay = upmMMA7660.new_floatp()
az = upmMMA7660.new_floatp()


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
	button = grove.GroveButton(0)
	print ""
	print ""
	time.sleep(1)
	print "Press The button to add the node to the network"
	while button.value() == 0:
		led.on()
		time.sleep(1)
	print "Add process in progress!!! please wait"
	led.off()

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
		#os.system("stty -F /dev/ttyMFD1 4800")
		#if not os.path.exists(GPS_ADDRESS):
		#	os.system("echo %s > %s" % (GPS_ON, EXPORT_ADDRESS))
	     #           os.system("echo out > %s" % GPS_DIRECTION_ADDRESS)
		
		#os.system("echo 1 > %s" % GPS_VALUE_ADDRESS)
		#time.sleep(1)
         #       os.system("echo 0 > %s" % GPS_VALUE_ADDRESS)
		#temp = grove.GroveTemp(TEMP_PIN)
		#light = grove.GroveLight(LIGHT_PIN)
		
		# Instantiate an MMA7660 on I2C bus 0
		#myDigitalAccelerometer = upmMMA7660.MMA7660(
         #  			upmMMA7660.MMA7660_I2C_BUS,
          #          upmMMA7660.MMA7660_DEFAULT_I2C_ADDR);
		
		# place device in standby mode so we can write registers
		myDigitalAccelerometer.setModeStandby()

		# enable 64 samples per second
		myDigitalAccelerometer.setSampleRate(upmMMA7660.MMA7660.AUTOSLEEP_64)

		# place device into active mode
		myDigitalAccelerometer.setModeActive()



		self._run = True
        def stop(self):
		#To turn off GPS
		#os.system("echo 1 > %s" % GPS_VALUE_ADDRESS)
         #       time.sleep(1)
          #      os.system("echo 0 > %s" % GPS_VALUE_ADDRESS)
                self._run = False
		#self.f.close()
        def run(self):
                print "\n", "-" * 15, "STARTING THREAD", "-" * 15
                #f = open("/dev/ttyMFD1")
		#streamreader = pynmea2.NMEAStreamReader(f)
		#a = 0
		while self._run:
			try:
				print "trying"
				#msg = streamreader.next()
				#Lat = int(msg.lat[:2]) + float(msg.lat[2:])/60    
				#Lon = int(msg.lon[:3]) + float(msg.lon[3:])/60
				myDigitalAccelerometer.getAcceleration(ax, ay, az)
    			#f_ax = upmMMA7660.floatp_value(ax) #formated ax
    			#f_ay = upmMMA7660.floatp_value(ay) #formated ay
    			#f_az = upmMMA7660.floatp_value(az) #formated az
    			#outputStr = ("x = {0}"
   				#"y = {1}"
    			#"z = {2}").format(upmMMA7660.floatp_value(ax),
    			#upmMMA7660.floatp_value(ay),
    			#upmMMA7660.floatp_value(az))
    			#print outputStr
    			#time.sleep(.5)
    			#outputStr = ("Acceleration: x = {0}"
    			#"g y = {1}"
    			#"g z = {2}g").format(upmMMA7660.floatp_value(ax),
    			#upmMMA7660.floatp_value(ay),
    			#upmMMA7660.floatp_value(az))
				#print Lat, Lon
				#print "%.4f%s,%.4f%s vs %s%s, %s%s" % (Lat, msg.lat_dir, Lon, msg.lon_dir, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir)
				statusLock.acquire(1)
				sensor_value["acceleration"] = "x = %.4f, y = %.4f, z = %.4f" % (ax, ay, az)
				#sensor_value["acceleration"] = outputStr 
				statusLock.release()
			except:			
				pass
			statusLock.acquire(1)
			sensor_value["temp"] = str(temp.value())
			sensor_value["light"] = str(light.value())
			#a += 0.1
			statusLock.release()
			print "\n", "-" * 15, "SENSORS UPDATED", "-" * 15
			print sensor_value
            #    f.close()
		return


#Program Start. Load node information
signal.signal(signal.SIGINT, signal_handler)
node_info, sensor_value, sensor_alarm  = init_env()
ssid = read_SSID()
add_process = False
#Definition of LED indicator output
led = grove.GroveLed(2)

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
	time.sleep(1) # for LED blinking
	led.on()
	error, json_data = add_request(ip)
	time.sleep(1) # for LED blinking
	led.off()
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
	
# -*- coding: utf-8 -*-
import pynmea2
import sys

f = open("/dev/ttyMFD1")
streamreader = pynmea2.NMEAStreamReader(f)
while 1:
	try:	
		for msg in streamreader.next():
			Lat = int(msg.lat[:2]) + float(msg.lat[2:])/60    
			Lon = int(msg.lon[:3]) + float(msg.lon[3:])/60
			#print Lat1
			#print Lat
			print "%.4f%s,%.4f%s vs %s%s, %s%s" % (Lat, msg.lat_dir, Lon, msg.lon_dir, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir)
	except KeyboardInterrupt:
		print "BYEEEE"
		sys.exit()		
	except:
		pass

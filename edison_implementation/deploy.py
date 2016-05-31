import pickle
import os
from sys import argv

script, deploy_mode = argv

MAIN_DIRECTORY = "/opt/NEGRAV/"
NODE_CONFIG = "/opt/NEGRAV/node.config"

IP="NULL"

if int(deploy_mode) == 1:
	print "\n", "-" * 15, "DEPLOYING NODE WITH GPS", "-" * 15
	
	#Sensor basic info
	GPS = ["4.34N","7.5W","2600m"]
	Type = "MN" #MN or SN
	S1={'name':'GPS',
        	'units': ['lat/long'],
        	'resolution':'100m',
        	'range': ['NULL','NULL'] }

	S2={'name':'random',
        	'units': ['R'],
        	'resolution':'1R',
        	'range': ['0R','100'] }

	S3={'name':'sin',
        	'units': ['degree'],
        	'resolution':'0.11deg',
        	'range': ['-50','50'] }

	sensors = [S1, S2, S3]
	
	#Sensor values
        sensor_value = {'GPS':"NULL", 'random':"NULL", 'sin':"NULL"}

        S1_alarm={'name':'GPS',
                'alarm': ["NULL","NULL"]}
        S2_alarm={'name':'random',
                'alarm': ["NULL","NULL"]}
        S3_alarm={'name':'sin',
                'alarm': ["NULL","NULL"]}
        sensor_alarms = [S1_alarm, S2_alarm, S3_alarm]

elif int(deploy_mode) == 2:
	print "\n", "-" * 15, "DEPLOYING STANDALONE NODE", "-" * 15

	#Sensor basic info
        Type = "SN" #MN or SN
        S1={'name':'random',
                'units': ['r'],
                'resolution':'1r',
                'range': ['0','100'] }

        S2={'name':'cos',
                'units': ['degree'],
                'resolution':'0.11deg',
                'range': ['-50','50'] }

        S3={'name':'sin',
                'units': ['degree'],
                'resolution':'0.11deg',
                'range': ['-50','50'] }

        sensors = [S1, S2, S3]

        #Sensor values
        sensor_value = {'random':"NULL", 'cos':"NULL", 'sin':"NULL"}

	S1_alarm={'name':'random',
                'alarm': ["NULL","NULL"]}
        S2_alarm={'name':'cos',
                'alarm': ["NULL","NULL"]}
        S3_alarm={'name':'sin',
                'alarm': ["NULL","NULL"]}
        sensor_alarms = [S1_alarm, S2_alarm, S3_alarm]


else:
	print "\n", "-" * 15, "DEPLOYING ARDUINO NODE", "-" * 15

	#Sensor basic info
	Type = "SN" #MN or SN
	S1={'name':'temp',
		'units': ['C'],
		'resolution':'1.5C',
		'range': ['-40C','125C'] }  

	S2={'name':'acceleration',
		'units': ['g'],
		'resolution':'0.01g',
		'range': ['-1.5g','1.5g'] }  
	
	S3={'name':'light',
		'units': ['lumen'],
		'resolution':'1lux',
		'range': ['-5lux','5lux'] }  

	sensors = [S1, S2, S3]

	#Sensor values
	sensor_value = {'temp':"NULL", 'acceleration':"NULL", 'light':"NULL"}


	S1_alarm={'name':'temp',
		'alarm': ["NULL","NULL"]}  

	S2_alarm={'name':'acceleration',
		'alarm': ["NULL","NULL"]}  

	S3_alarm={'name':'light',
		'alarm': ["NULL","NULL"]} 

	sensor_alarms = [S1_alarm, S2_alarm, S3_alarm]



node_info = {'node_ip': IP, 'type': Type, 'sensor':sensors}

if not os.path.exists(MAIN_DIRECTORY):
    os.makedirs(MAIN_DIRECTORY)      

f = open(NODE_CONFIG, 'w')
pickle.dump((node_info, sensor_value, sensor_alarms), f)
f.close()

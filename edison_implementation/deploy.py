import pickle
import os

MAIN_DIRECTORY = "/opt/NEGRAV/"
NODE_CONFIG = "/opt/NEGRAV/node.config"

IP="NULL"
GPS = ["4.34N","7.5W","2600m"]
Type = "SN" #MN or SN
S1={'name':'temp',
	'units': ['c','F','k'],
	'resolution':'1c',
	'range': ['-50F','50F'] }  

S2={'name':'humidity',
	'units': ['c','F','k'],
	'resolution':'1c',
	'range': ['-50F','50F'] }  

S3={'name':'presion',
	'units': ['c','F','k'],
	'resolution':'1c',
	'range': ['-50F','50F'] }  

sensors = [S1, S2, S3]

S1_alarm={'name':'temp',
	'alarm': ['0','10']}  

S2_alarm={'name':'humidity',
	'alarm': ['0','10'],
	'resolution':'1c',
	'range': ['-50F','50F'] }  

S3_alarm={'name':'presion',
	'units': ['c','F','k'],
	'resolution':'1c',
	'range': ['-50F','50F'] } 


sensor_alarms = [S1_alarm, S2_alarm, S3_alarm]

node_info = {'node_ip': IP, 'GPS':GPS, 'type': Type, 'sensor':sensors}

if not os.path.exists(MAIN_DIRECTORY):
    os.makedirs(MAIN_DIRECTORY)      

f = open(NODE_CONFIG, 'w')
pickle.dump(node_info, f)
f.close()
import pickle
import os

MAIN_DIRECTORY = "/opt/NEGRAV/"
NODE_DB = "/opt/NEGRAV/node.db" #database of all the nodes in the network

node_database = []

if not os.path.exists(MAIN_DIRECTORY):
    os.makedirs(MAIN_DIRECTORY)      

f = open(NODE_DB, 'w')
pickle.dump(node_database, f)
f.close()
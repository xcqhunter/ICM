# encoding=utf-8
import sys,time
sys.path.insert(0, "..")
from opcua import Client

import datetime

import socket  
import fcntl
import struct
import traceback


def get_local_ip(ifname):

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
	inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))  
	ret = socket.inet_ntoa(inet[20:24]) 

	return ret 

if __name__ == "__main__":

 

    client = Client("opc.tcp://" + get_local_ip("eth0") + ":4840/freeopcua/server/")
    #client = Client("opc.tcp://127.0.0.1:4840/freeopcua/server/")
    #client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    try:
        res = client.connect()

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        print("Objects node is: ", root)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        print("Children of root are: ", root.get_children())

        # get a specific node knowing its node id
        #var = client.get_node(ua.NodeId(1002, 2))
        #var = client.get_node("ns=3;i=2002")
        #print(var)
        #var.get_data_value() # get value of node as a DataValue object
        #var.get_value() # get value of node as a python builtin
        #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #var.set_value(3.9) # set node value using implicit data type

        # Now getting a variable node using its browse path
        while(1):
            myvar = root.get_child(["0:Objects", "2:obj_modbusDevInfoList", "2:v_modbusDevInfoList"])
            obj = root.get_child(["0:Objects", "2:obj_modbusDevInfoList"])

            print("myvar is: ", myvar)
            print("myobj is: ", obj)
            
            # Stacked myvar access
            print("myvar is: ", root.get_children()[0].get_children()[1].get_variables()[0].get_value())
            time.sleep(2)

    finally:
        client.disconnect()




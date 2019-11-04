# encoding=utf-8
import sys
sys.path.insert(0, "..")
import time
#from opcua import ua, Server
from opcua import Server

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

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://" + get_local_ip("eth0") + ":4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "MyObject")
    myvar = myobj.add_variable(idx, "MyVariable", 6.7)
    myvar.set_writable()    # Set MyVariable to be writable by clients

    # starting!
    server.start()
    
    try:
        count = 0
        while True:
            dateInfo=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            myvar.set_value(dateInfo)
            time.sleep(1)
            count += 0.1
            myvar.set_value(count)
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()


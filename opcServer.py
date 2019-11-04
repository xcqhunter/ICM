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




#-*- coding: UTF-8 -*-
#!/usr/bin/python

import sys
import struct
import modbus_tk.defines as cst
import modbus_tk.modbus
import modbus_tk.modbus_tcp
import string
import time
import threading
import socket
import logging
import Log

import os
import re
import platform
import subprocess
import datetime
import OpenOPC
import traceback
import sysInfoManager

import json


class opcServer():

    modeName="opcServer"
    log = Log.Log

    status = 0
    
    def init(self):
		
	self.sysTopInfo=sysInfoManager.sysInfoManager

	self.modbusDevInfoList = self.sysTopInfo.getInfo("modbusDevInfoList")
	self.opcInfoList = self.sysTopInfo.getInfo("opcInfoList")
	self.lzbusIpInfoList = self.sysTopInfo.getInfo("lzbusIpInfoList")
	self.snmpInfoList = self.sysTopInfo.getInfo("snmpInfoList")
	

    def get_local_ip(self, ifname):

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
	inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))  
	ret = socket.inet_ntoa(inet[20:24]) 

	return ret
    def user_manager(self, isession, userName, password):
        if userName in ("admin") and password in ("Aa123456"):
            return True
        return False
    
    def serverLoop(self):

 	self.log.Info(self.opcInfoList)

	# setup our server
	server = Server()
	server.set_endpoint("opc.tcp://" + self.get_local_ip("eth0") + ":4840/freeopcua/server/")

	# setup our own namespace, not really necessary but should as spec
	uri = "http://examples.freeopcua.github.io"
	idx = server.register_namespace(uri)
        
        server.user_manager.set_user_manager(self.user_manager)
	# get Objects node, this is where we should put our nodes
	objects = server.get_objects_node()

	# populating our address space
	obj_modbusDevInfoList = objects.add_object(idx, "obj_modbusDevInfoList")
	obj_opcInfoList = objects.add_object(idx, "obj_opcInfoList")
	obj_lzbusIpInfoList = objects.add_object(idx, "obj_lzbusIpInfoList")
	obj_snmpInfoList = objects.add_object(idx, "obj_snmpInfoList")
	
        obj_dev1 = objects.add_object(idx, "obj_173_12_10_138")
        obj_dev2 = objects.add_object(idx, "obj_173_12_10_139")

	v_modbusDevInfoList = obj_modbusDevInfoList.add_variable(idx, "v_modbusDevInfoList", "")
	v_opcInfoList = obj_opcInfoList.add_variable(idx, "v_opcInfoList", "")
	v_lzbusIpInfoList = obj_lzbusIpInfoList.add_variable(idx, "v_lzbusIpInfoList", "")
	v_snmpInfoList = obj_snmpInfoList.add_variable(idx, "v_snmpInfoList", "")
	
        d1_ip = obj_dev1.add_variable(idx, "ID", "173.12.10.138")
        d1_type = obj_dev1.add_variable(idx, "TYPE", "1")
        d1_powerstatus = obj_dev1.add_variable(idx, "POWERSTAUS", "on")
        d1_netstatus = obj_dev1.add_variable(idx, "NETSTATUS", "on")
        d1_cpu1_per = obj_dev1.add_variable(idx, "CPU1_PER", "70")
        d1_cpu2_per = obj_dev1.add_variable(idx, "CPU2_PER", "50")
        d1_cpu3_per = obj_dev1.add_variable(idx, "CPU3_PER", "30")
        d1_cpu4_per = obj_dev1.add_variable(idx, "CPU4_PER", "10")
        d1_mem_total = obj_dev1.add_variable(idx, "MEM_TOTAL", "82300000")
        d1_disk_total = obj_dev1.add_variable(idx, "DISK_TOTAL", "70")



        d2_type = obj_dev2.add_variable(idx, "TYPE", "1")
        d2_powerstatus = obj_dev2.add_variable(idx, "POWERSTAUS", "on")
        d2_netstatus = obj_dev2.add_variable(idx, "NETSTATUS", "on")
        d2_cpu1_per = obj_dev2.add_variable(idx, "CPU1_PER", "70")
        d2_cpu2_per = obj_dev2.add_variable(idx, "CPU2_PER", "50")
        d2_cpu3_per = obj_dev2.add_variable(idx, "CPU3_PER", "30")
        d2_cpu4_per = obj_dev2.add_variable(idx, "CPU4_PER", "10")
        d2_mem_total = obj_dev2.add_variable(idx, "MEM_TOTAL", "82300000")
        d2_disk_total = obj_dev2.add_variable(idx, "DISK_TOTAL", "70")



	# starting!
	server.start()

	while True:
		dateInfo=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
		v_modbusDevInfoList.set_value(json.dumps(self.modbusDevInfoList))
		v_opcInfoList.set_value(json.dumps(self.opcInfoList))
		v_lzbusIpInfoList.set_value(json.dumps(self.lzbusIpInfoList))
		v_snmpInfoList.set_value(json.dumps(self.snmpInfoList))
	
                
                d1_ip.set_value("173.12.10.138")
		d1_type.set_value("1")
		d1_powerstatus.set_value("on")
		d1_netstatus.set_value("on")
		d1_cpu1_per.set_value("70")
		d1_cpu2_per.set_value("50")
		d1_cpu3_per.set_value("30")
		d1_cpu4_per.set_value("10")
		d1_mem_total.set_value("82300000")
		d1_disk_total.set_value("70")



		d2_type.set_value("1")
		d2_powerstatus.set_value("on")
		d2_netstatus.set_value("on")
		d2_cpu1_per.set_value("70")
		d2_cpu2_per.set_value("50")
		d2_cpu3_per.set_value("30")
		d2_cpu4_per.set_value("10")
		d2_mem_total.set_value("82300000")
		d2_disk_total.set_value("70")



                
                time.sleep(60)
 
    def start(self):
        if self.status == 0:		
            self.status = 1	
            self.thread = threading.Thread(target=self.serverLoop)
            self.thread.start()

opcServer = opcServer()



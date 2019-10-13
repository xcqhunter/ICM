#-*- coding: UTF-8 -*-
#!/usr/bin/python
import sys
import json
import threading
import os
from copy import deepcopy

import logging
import Log
import time
import threading
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
import modbus_tk.modbus_tcp as modbus_tcp
import random

import sysInfoManager

import socket  
import fcntl
import struct
import traceback

class modbusServer():

	log = Log.Log
	lock = threading.Lock()

	status = 0

	def init(self):
		self.sysTopInfo=sysInfoManager.sysInfoManager
		self.modbusServerInfoList = self.sysTopInfo.getInfo("modbusServerInfoList")

	def get_local_ip(self, ifname):

		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
		inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))  
		ret = socket.inet_ntoa(inet[20:24]) 
 
		return ret  

	def start_server(self):
		try:
			# server里的Ip和端口，注意开放相应的端口
			SERVER = modbus_tk.modbus_tcp.TcpServer(address=self.get_local_ip("eth0"), port=502)
			# 服务启动
			SERVER.start()
			# 建立第一个从机
			SLAVE1 = SERVER.add_slave(1)

			for i in range(len(self.modbusServerInfoList)):
				info = self.modbusServerInfoList[i]
				SLAVE1.add_block(info['regLable'], 
						cst.HOLDING_REGISTERS, 
						int(info['regStart']), 
						int(info['size']))
			
		except Exception as e:
			self.log.Info(traceback.print_exc())
			self.log.Info(e)

	def list_convert_ord(self, obj_list):
		for i in range(len(obj_list)):
			obj_list[i] = ord(obj_list[i])
		return obj_list

	def write_slave_info(self, master, startaddr, obj_list):

		obi_list_size = len(obj_list)

		master.execute(1, 
				16, 
				startaddr, 
				1,
				(obi_list_size,))

		startaddr = startaddr + 1

		list_tmp = obj_list

		
		while(len(list_tmp) >= 100):
			self.log.Info(startaddr)
			master.execute(1, 
					16, 
					startaddr, 
					100,
					list_tmp[0:100])
			startaddr = startaddr + 100
			list_tmp = list_tmp[100:len(list_tmp)]

		self.log.Info(startaddr)
		master.execute(1, 
				16, 
				startaddr, 
				len(list_tmp),
				list_tmp)
		

	def write_value(self):
		self.start_server()
		while True:
			try:
				time.sleep(5)
				master=modbus_tk.modbus_tcp.TcpMaster(host=self.get_local_ip("eth0"), port=502)
				master.set_timeout(5.0)
				for i in range(len(self.modbusServerInfoList)):
					info = self.modbusServerInfoList[i]
					
					#将数据结构写入寄存器
					obj = json.dumps(self.sysTopInfo.getInfo(info['regLable']))
					self.log.Info(info['regLable'])	
				
					obj_list = list(obj)
					obj_list = self.list_convert_ord(obj_list)
					self.write_slave_info(master,int(info['regStart']), obj_list)
			

			
				self.log.Info("==== set_values...")
				master._do_close()

			except Exception as e:
				self.log.Info(traceback.print_exc())
				self.log.Info(e)

	def start(self):
		if self.status == 0:		
			self.status = 1	
			self.thread = threading.Thread(target=self.write_value)
			self.thread.start()


modbusServer = modbusServer()






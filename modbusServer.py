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

class modbusServer():

	log = Log.Log
	lock = threading.Lock()

	status = 0

	def init(self):
		self.sysTopInfo=sysInfoManager.sysInfoManager
		self.modbusDevInfoList = self.sysTopInfo.getInfo("modbusServerInfoList")

	def start_server(self):
		try:
			# server里的Ip和端口，注意开放相应的端口
			SERVER = modbus_tk.modbus_tcp.TcpServer(address="", port=502)
			# 服务启动
			SERVER.start()
			# 建立第一个从机
			SLAVE1 = SERVER.add_slave(1)
			SLAVE1.add_block('modbusDevInfoList', cst.HOLDING_REGISTERS, 0, 2000)#地址0，长度4
			SLAVE1.add_block('routeDevInfoList', cst.HOLDING_REGISTERS, 2000, 2000)#地址0，长度4
			SLAVE1.add_block('opcserverInfoList', cst.HOLDING_REGISTERS, 4000, 2000)#地址0，长度4
			SLAVE1.add_block('lzbusIpInfoList', cst.HOLDING_REGISTERS, 6000, 2000)#地址0，长度4
			
		except Exception as e:
			self.log.Info(e)

	def list_convert_ord(self, obj_list):
		for i in range(len(obj_list)):
			obj_list[i] = ord(obj_list[i])
		return obj_list

	def write_slave_info(self, master, startaddr, obj_list):

		obi_list_size = len(obj_list)

		master.execute(1, 
				3, 
				startaddr, 
				1,
				obi_list_size)

		startaddr = startaddr + 1

		list_tmp = obj_list

		
		while(len(list_tmp) >= 100):
			self.log.Info(startaddr)
			master.execute(1, 
					3, 
					startaddr, 
					100,
					list_tmp[0:100])
			startaddr = startaddr + 100
			list_tmp = list_tmp[100:len(list_tmp)]
			
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
				master=modbus_tk.modbus_tcp.TcpMaster(host="127.0.0.1", port=502)
				master.set_timeout(5.0)

				#将数据结构写入寄存器
				obj = json.dumps(self.sysTopInfo.getInfo("modbusDevInfoList"))
				obj_list = list(obj)
				obj_list = self.list_convert_ord(obj_list)				
				self.write_slave_info(master,0, obj_list)

				obj = json.dumps(self.sysTopInfo.getInfo("snmpInfoList"))
				obj_list = list(obj)
				obj_list = self.list_convert_ord(obj_list)				
				self.write_slave_info(master,2000, obj_list)

				obj = json.dumps(self.sysTopInfo.getInfo("opcInfoList"))
				obj_list = list(obj)
				obj_list = self.list_convert_ord(obj_list)				
				self.write_slave_info(master,4000, obj_list)

				obj = json.dumps(self.sysTopInfo.getInfo("lzbusIpInfoList"))
				obj_list = list(obj)
				obj_list = self.list_convert_ord(obj_list)				
				self.write_slave_info(master,6000, obj_list)

			
				self.log.Info("==== set_values...")
				master._do_close()

			except Exception as e:
				self.log.Info(e)

	def start(self):
		if self.status == 0:		
			self.status = 1	
			self.thread = threading.Thread(target=self.write_value)
			self.thread.start()


modbusServer = modbusServer()






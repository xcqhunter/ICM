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
import datetime

import sysInfoManager

class collectModbusInfo():

	modeName="collectModbusInfo"
	log = Log.Log

	status = 0
    
	def init(self):

		self.sysTopInfo=sysInfoManager.sysInfoManager
		self.modbusDevInfoList = self.sysTopInfo.getInfo("modbusDevInfoList")
	
	def collectInfo(self):
		while True:
			try:
				for i in range(len(self.modbusDevInfoList)):
					modbusDevInfo = self.modbusDevInfoList[i]
					# 连接MODBUS设备
					master=modbus_tk.modbus_tcp.TcpMaster(host=modbusDevInfo['modbusDevIp'],
										 port=int(modbusDevInfo['modbusDevPort']))
					master.set_timeout(5.0)
					regInfoList = modbusDevInfo['regInfo']
			
					for j in range(len(regInfoList)):				
						# 读保持寄存器
						self.log.Info(regInfoList[j]['regStart'])
						self.log.Info(int(regInfoList[j]['regStart']))
						value = master.execute(int(regInfoList[j]['slaveId']), 
									int(regInfoList[j]['funcCode']), 
									int(regInfoList[j]['regStart']), 
									int(regInfoList[j]['size']))
						regInfoList[j]['regContent'] = value
					modbusDevInfo['regInfo'] = regInfoList

					#存入日期
					dateInfo=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
					modbusDevInfo['Date'] = dateInfo

					self.modbusDevInfoList[i] = modbusDevInfo
					#存入数据信息管理模块
					self.sysTopInfo.setInfoByKey("modbusDevInfoList", self.modbusDevInfoList)
					master._do_close()
				

			except socket.timeout:   # connection timeout exception
				self.log.Info("modbusDev is not connected==========")
				continue
			except Exception as e:
				self.log.Info(e)
			finally:
				self.log.Info(self.sysTopInfo.getInfo("modbusDevInfoList"))
				time.sleep(6)
 
	def start(self):
		if self.status == 0:		
			self.status = 1	
			self.thread = threading.Thread(target=self.collectInfo)
			self.thread.start()

collectModbusInfo = collectModbusInfo()

 

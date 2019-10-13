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

class collectOpcInfo():

    modeName="collectOpcInfo"
    log = Log.Log

    status = 0
    
    def init(self):
		
	self.sysTopInfo=sysInfoManager.sysInfoManager
	self.opcInfoList = self.sysTopInfo.getInfo("opcInfoList")
	
    def colectInfo(self):
 	self.log.Info(self.opcInfoList)
	while True:
		try:
			for i in range(len(self.opcInfoList)):
				opchost=self.opcInfoList[i]['opchost']
				opcserver=self.opcInfoList[i]['opcserver']
				ItemList=self.opcInfoList[i]['ItemList']

				opc = OpenOPC.open_client(opchost)
				opc.connect(opcserver, opchost)

				for j in range(len(ItemList)):
					ItemList[j]['value'] = opc.read(ItemList[j]['Item'])
				
				self.opcInfoList[i]['ItemList'] = ItemList
				#存入日期
				dateInfo=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
				self.opcInfoList[i]['Date'] = dateInfo

				opc.close()

			self.log.Info(self.opcInfoList)
			#存入数据信息管理模块
			self.sysTopInfo.setInfoByKey("opcInfoList", self.opcInfoList)

		except Exception, e: 
			self.log.Info(traceback.print_exc())
			self.log.Info(e)

		time.sleep(60)
 
    def start(self):
        if self.status == 0:		
            self.status = 1	
            self.thread = threading.Thread(target=self.colectInfo)
            self.thread.start()

collectOpcInfo = collectOpcInfo()

 


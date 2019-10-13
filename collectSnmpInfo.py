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
import traceback
import sysInfoManager

class collectSnmpInfo():

    modeName="collectSnmpInfo"
    log = Log.Log

    status = 0
    
    def init(self):
		
		self.sysTopInfo=sysInfoManager.sysInfoManager
		self.snmpInfoList = self.sysTopInfo.getInfo("snmpInfoList")
	
    def snmpWalk(self, version, agentIp, community, oid):
	cmd = "snmpwalk -v " + version + " -c "+community+" "+agentIp+" "+oid
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        #result = os.popen("snmpwalk -v " + version + " -c "+community+" "+agentIp+" "+oid, os.O_RDWR)
	result = p.stdout.read()
	result = result[result.find("=")+1:len(result)]
	return result

    def colectInfo(self):
 
	
	while True:
		try:
			for i in range(len(self.snmpInfoList)):

				snmpInfo = self.snmpInfoList[i]
				oidlist = snmpInfo['oidList']
				for j in range(len(oidlist)):
					oid = oidlist[j]['oid']
					oidlist[j]['value'] = self.snmpWalk(snmpInfo['version'], 
									snmpInfo['agentIp'], 
									snmpInfo['community'], 
									oid)
				snmpInfo['oidList'] = oidlist
				#存入日期
				dateInfo=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
				snmpInfo['Date'] = dateInfo

				self.snmpInfoList[i] = snmpInfo

			self.log.Info(self.snmpInfoList)
			#存入数据信息管理模块
			self.sysTopInfo.setInfoByKey("snmpInfoList", self.snmpInfoList)

		except Exception, e: 
			self.log.Info(traceback.print_exc())
			self.log.Info(e)

		time.sleep(60)
 
    def start(self):
        if self.status == 0:		
            self.status = 1	
            self.thread = threading.Thread(target=self.colectInfo)
            self.thread.start()

collectSnmpInfo = collectSnmpInfo()

 


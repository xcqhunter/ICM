#-*- coding: UTF-8 -*-
#!/usr/bin/python

import sys
import json
import threading
import os
from copy import deepcopy
import logging
import Log


sys.path.append("cfg")
import modbusDevInfoList
import modbusServerInfoList
import lzbusIpInfoList
import opcInfoList
import snmpInfoList

class sysInfoManager():

	topInfo = {
		'modbusDevInfoList':[],
		'opcInfoList':[],
		'lzbusIpInfoList':[],
		'snmpInfoList':[],
		'modbusServerInfoList':[],

	}

	log = Log.Log

	lock = threading.Lock()

	def init(self):
		self.setInfoByKey("modbusDevInfoList", modbusDevInfoList.modbusDevInfoList)
		self.setInfoByKey("modbusServerInfoList", modbusServerInfoList.modbusServerInfoList)
		self.setInfoByKey("lzbusIpInfoList", lzbusIpInfoList.lzbusIpInfoList)
		self.setInfoByKey("opcInfoList", opcInfoList.opcInfoList)
		self.setInfoByKey("snmpInfoList", snmpInfoList.snmpInfoList)

	def setInfoByKey(self, key, objInfo):
	        self.lock.acquire()
	
	        self.topInfo[key]=objInfo

	        self.lock.release()

	def getInfo(self, key):
	        info = {}
	        if key in self.topInfo:
	            info = deepcopy(self.topInfo[key])
	        return info


sysInfoManager = sysInfoManager()






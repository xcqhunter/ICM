#-*- coding: UTF-8 -*-
#!/usr/bin/python

import time
import logging
import Log


import sysInfoManager
import collectModbusInfo
import collectSnmpInfo
import collectLzbusIpInfo
import modbusServer
import NBIOT
import collectOpcInfo
import opcServer


if __name__ == "__main__":
	log = Log.Log
	log.Init("console&file",logging.DEBUG)

	#初始化数据结构
	sysTopInfo = sysInfoManager.sysInfoManager
	sysTopInfo.init()
	log.Info(sysTopInfo.getInfo("modbusDevInfoList"))

	#采集modbusDev信息
	modbusInfo = collectModbusInfo.collectModbusInfo
	modbusInfo.init()
	#modbusInfo.start()

	#采集snmp设备信息
	snmpInfo = collectSnmpInfo.collectSnmpInfo
	snmpInfo.init()
	snmpInfo.start()

	#采集lzbusIp设备状态信息
	lzbusIpInfo = collectLzbusIpInfo.collectLzbusIpInfo
	lzbusIpInfo.init()
	#lzbusIpInfo.start()

	#启动modbusServer
	msserver = modbusServer.modbusServer
	msserver.init()
	#msserver.start()

	#NBIOT模块初始化
	nb = NBIOT.NBIOT
	nb.init()
	#nb.start()

	#opc模块初始化
	opcInfo = collectOpcInfo.collectOpcInfo
	opcInfo.init()
	#opcInfo.start()


	#opcServer模块初始化
	opc_server = opcServer.opcServer
	opc_server.init()
	opc_server.start()

	while True:
		time.sleep(1)






#-*- coding: UTF-8 -*-
#!/usr/bin/env python

import serial
import thread
import logging
import Log
import time
import threading
import subprocess
import sysInfoManager
import datetime
import traceback

class collectLzbusIpInfo():

	status = 0
	
	recive_buf = ""

	log = Log.Log

	lock = threading.Lock()

	def init(self):
		try:
			self.serial = serial.Serial("/dev/ttyS5",9600,timeout=0.2)#Linux系统使用com1口连接串行口
			self.serial.open() #打开端口
		except Exception as e:
                        self.log.Info(traceback.print_exc())
                        self.log.Info(e)
		
		self.READ_LZBUS_FLAG = 0
		self.WRITE_LZBUS_FLAG = 1

		self.sysTopInfo=sysInfoManager.sysInfoManager
		self.lzbusIpInfoList = self.sysTopInfo.getInfo("lzbusIpInfoList")
	
	def generate_lzbus_frame(self, devAddr, regAddr, rw, size, data):
		payload = "5520"
		payload = payload + "%02x"%(devAddr)
		if rw:
			data_sign = 0x80 + size - 1
			payload = payload + "%02x"%(data_sign)
			payload = payload + "%02x"%(regAddr)
			payload = payload + data
		else:
			data_sign = 0x00 + size - 1
			payload = payload + "%02x"%(data_sign)
			payload = payload + "%02x"%(regAddr)
		
		sum_tmp = 0
		for i in range(len(payload)/2):
			sum_tmp = sum_tmp + int(payload[i*2:i*2+2],16)
		
                sum_tmp = sum_tmp%0x100

		lzbus_frame = payload + "%02x"%(sum_tmp)
	
		return lzbus_frame

	def handle_lzbus_frame(self, lzbus_frame):
		#校验帧是否正确
                if lzbus_frame == "":
                    self.log.Info("lzbus_frame is ""!!!")
                    return    
                self.log.Info(lzbus_frame)
		sum_byte = int(lzbus_frame[len(lzbus_frame)-2:len(lzbus_frame)],16)
		payload = lzbus_frame[0:len(lzbus_frame)-2]
		sum_tmp = 0
		

		for i in range(len(payload)/2):
			sum_tmp = sum_tmp + int(payload[i*2:i*2+2],16)
		
                sum_tmp = sum_tmp%0x100
		
                if sum_byte != sum_tmp:
			self.log.Info("check sum err !!!")
			return

		#解析数据
		devAddr = int(payload[2*2:2*2+2], 16)
		data_sign = int(payload[3*2:3*2+2], 16)
		regAddr = int(payload[4*2:4*2+2], 16)

		byte_size = data_sign%16 + 1
		self.log.Info(devAddr)
		self.log.Info(byte_size)
		self.log.Info(regAddr)
		#此设备为主设备，不处理读命令
		if data_sign&0x80 == 0:
			self.log.Info("lzbus_frame is read type not deal !!!")
			return
		
		regValueList = payload[5*2:5*2+byte_size*2]

		#设备的数据结构
		index = 0
		for i in range(len(self.lzbusIpInfoList)):
			if self.lzbusIpInfoList[i]['lzDevId'] == devAddr:
				index = i
				break
			if self.lzbusIpInfoList[i]['lzDevId'] == "":
				self.lzbusIpInfoList[i]['lzDevId'] = devAddr
				index = i
				break

		if regAddr == 0x10:
                        self.log.Info(regValueList)
                        regValue = int(regValueList[0:2], 16)
			if len(regValueList) > 0:
				regValueList = regValueList[2:len(regValueList)]
				regAddr = regAddr + 1
			self.log.Info("=== regValue ===")
			self.log.Info(regValue)
			#Din5-0
                        self.lzbusIpInfoList[index]['Dio5']['Din'] = "on" if (regValue&0x80) else "off"
			self.lzbusIpInfoList[index]['Dio4']['Din'] = "on" if (regValue&0x40) else "off"
			self.lzbusIpInfoList[index]['Dio3']['Din'] = "on" if (regValue&0x20) else "off"
			self.lzbusIpInfoList[index]['Dio2']['Din'] = "on" if (regValue&0x10) else "off" 
			self.lzbusIpInfoList[index]['Dio1']['Din'] = "on" if (regValue&0x08) else "off"
			self.lzbusIpInfoList[index]['Dio0']['Din'] = "on" if (regValue&0x04) else "off"
	
			#Dout1-0
			self.lzbusIpInfoList[index]['Dio1']['Dout'] = "on" if (regValue&0x02) else "off"
			self.lzbusIpInfoList[index]['Dio0']['Dout'] = "on" if (regValue&0x01) else "off"
    			#存入日期
			dateInfo=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
			self.lzbusIpInfoList[index]['Date'] = dateInfo

                        #存入数据信息管理模块
                        self.sysTopInfo.setInfoByKey("lzbusIpInfoList", self.lzbusIpInfoList)
                        self.log.Info(self.lzbusIpInfoList)

		if regAddr == 0x11:
                        self.log.Info(regValueList)
                        regValue = int(regValueList[0:2], 16)
			if len(regValueList) > 0:
				regValueList = regValueList[2:len(regValueList)]
				regAddr = regAddr + i
			self.log.Info(regValue)
			#Dout5-2
			self.lzbusIpInfoList[index]['Dio5']['Dout'] = "on" if (regValue&0x08) else "off"
			self.lzbusIpInfoList[index]['Dio4']['Dout'] = "on" if (regValue&0x04) else "off"
			self.lzbusIpInfoList[index]['Dio3']['Dout'] = "on" if (regValue&0x02) else "off"
			self.lzbusIpInfoList[index]['Dio2']['Dout'] = "on" if (regValue&0x01) else "off"

    			#存入日期
			dateInfo=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
			self.lzbusIpInfoList[index]['Date'] = dateInfo

		        #存入数据信息管理模块
		        self.sysTopInfo.setInfoByKey("lzbusIpInfoList", self.lzbusIpInfoList)
                        self.log.Info(self.lzbusIpInfoList)

	def handle_lzbus_info(self):
                while True:
			while(len(self.recive_buf)):
		                self.lock.acquire()
		                #查找 帧头 0x55 0x20
		                self.log.Info(self.recive_buf)
		                if self.recive_buf.find("5520") > 0:
		                        #去除 帧头 前多余信息
		                        self.recive_buf = self.recive_buf[self.recive_buf.index("5520")-1:len(self.recive_buf)]
		                #根据 协议域 判断帧是否接收完
		                if self.recive_buf.find("5520") == 0:
		                        #一帧数据接收完，则处理接收信息 目前只处理数据长度
		                        if len(self.recive_buf) >= 7:
		                                frame_size = int(self.recive_buf[3*2:3*2+2])%0x10 + 1 + 6
		                                if len(self.recive_buf) >= frame_size:
		                                        lzbus_frame = self.recive_buf[0:frame_size*2]
		                                        self.recive_buf = self.recive_buf[frame_size*2:len(self.recive_buf)]
		                                        self.handle_lzbus_frame(lzbus_frame)

		                self.lock.release()
                        time.sleep(10)
        def read_lzbus_info(self):
		while True:
			#读取串口数据
                        try:
			        char = self.serial.read(1)
                                if char != "":
                                        str_tmp = "%02x"%(ord(char))
			                #存入list
		                        self.lock.acquire()
			                self.recive_buf = self.recive_buf + str_tmp
		                        self.lock.release()
                        except Exception as e:
			        self.log.Info(e)

        def send_lzbus_frame(self, lzbus_frame):
                for i in range(len(lzbus_frame)/2):
                        self.serial.write(chr(int(lzbus_frame[i*2:i*2+2], 16)))

        def write_lzbus_frame(self):
		while True:
			#定时采集lzbus电源状态信息
			lzbus_frame = self.generate_lzbus_frame(0xff, 0x10, self.READ_LZBUS_FLAG, 3, "")
                        self.send_lzbus_frame(lzbus_frame)

			#定时采集设备网络状态信息 是否能ping通
			self.update_ip_status()

			time.sleep(60)

	def get_Ip_status(self, Ip):
		cmd = "ping " + Ip + " -c 1 -W 1"
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		result = p.stdout.read()
		keystring = "transmitted, "
		if result.find("transmitted, ") < len(result):
			result = result[result.find(keystring)+len(keystring)+1:result.find(keystring)+len(keystring)+2]

		if result == '1':
			ret = 'ok'
		else:
			ret = 'err'
		return ret
			
	def update_ip_status(self):
		lzbusInfoList = self.lzbusIpInfoList
		for i in range(len(lzbusInfoList)):
			lzbusInfo = lzbusInfoList[i]
			lzDevId = lzbusInfo['lzDevId']
			regValue = 0

			lzbusInfo['Dio5']['NetStatus'] == self.get_Ip_status(lzbusInfo['Dio5']['DevIp'])
			lzbusInfo['Dio4']['NetStatus'] == self.get_Ip_status(lzbusInfo['Dio4']['DevIp'])
			lzbusInfo['Dio3']['NetStatus'] == self.get_Ip_status(lzbusInfo['Dio3']['DevIp'])
			lzbusInfo['Dio2']['NetStatus'] == self.get_Ip_status(lzbusInfo['Dio2']['DevIp'])
			lzbusInfo['Dio1']['NetStatus'] == self.get_Ip_status(lzbusInfo['Dio1']['DevIp'])
			lzbusInfo['Dio0']['NetStatus'] == self.get_Ip_status(lzbusInfo['Dio0']['DevIp'])


	def set_lzbus_status(self):
		lzbusInfoList = self.lzbusIpInfoList
		for i in range(len(lzbusInfoList)):
			lzbusInfo = lzbusInfoList[i]
			lzDevId = lzbusInfo['lzDevId']
			regValue = 0

			if lzbusInfo['Dio5']['Dout'] == "on":
				regValue = regValue + 0x20
			if lzbusInfo['Dio4']['Dout'] == "on":
				regValue = regValue + 0x10
			if lzbusInfo['Dio3']['Dout'] == "on":
				regValue = regValue + 0x08
			if lzbusInfo['Dio2']['Dout'] == "on":
				regValue = regValue + 0x04
			if lzbusInfo['Dio1']['Dout'] == "on": 
				regValue = regValue + 0x02
			if lzbusInfo['Dio0']['Dout'] == "on": 
				regValue = regValue + 0x01

			lzbus_frame = self.generate_lzbus_frame(lzDevId, 0x11, self.WRITE_LZBUS_FLAG, 1, "%02x"%(regValue))
                        self.send_lzbus_frame(lzbus_frame)

	def start(self):
		if self.status == 0:
			self.status = 1	
			#启动接收数据线程
			self.thread = threading.Thread(target=self.read_lzbus_info)
			self.thread.start()
			#启动处理数据线程
			self.thread = threading.Thread(target=self.handle_lzbus_info)
			self.thread.start()
			#启动定时发送查询命令线程
			self.thread = threading.Thread(target=self.write_lzbus_frame)
			self.thread.start()


collectLzbusIpInfo = collectLzbusIpInfo()









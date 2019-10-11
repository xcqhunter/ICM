#-*- coding: UTF-8 -*-
#!/usr/bin/env python

import serial
import thread
import logging
import Log
import time
import threading

import sysInfoManager

class NBIOT():

	status = 0
	
	recive_buf = ""

	log = Log.Log

	lock = threading.Lock()

	def init(self):
		try:
			self.serial = serial.Serial("/dev/ttyS1",115200,timeout=0.5)#Linux系统使用com1口连接串行口
			self.serial.open() #打开端口
		except Exception as e:
			self.log.Info(e)
		
	
	def recive_info(self):
		protocol_field = ''
		while True:
			#读取串口数据
			char = self.serial.read(1)
			if char:
				self.log.Info(char)
				#存入list
				self.lock.acquire()
				self.recive_buf = self.recive_buf + char
				self.lock.release()

	
	def write_AT_CMD(self, at_cmd):

			self.serial.write(at_cmd+"\r\n")

	
        def start(self):
		if self.status == 0:
			self.status = 1	
			#启动接收数据线程
			self.thread = threading.Thread(target=self.recive_info)
			self.thread.start()
                while True:
		        self.write_AT_CMD("AT")
		        self.write_AT_CMD("AT+CSQ")
		        time.sleep(2)

			#启动处理数据线程
			#self.thread = threading.Thread(target=self.handle_lzbus_info)
			#self.thread.start()
			#启动定时发送查询命令线程
			#self.thread = threading.Thread(target=self.write_lzbus_frame)
			#self.thread.start()


NBIOT = NBIOT()









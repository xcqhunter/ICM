#-*- coding: UTF-8 -*-
#!/usr/bin/python

#FATAL—5
#ERROR—4
#WARNING—3
#INFO—2
#DEBUG—1


import logging
import threading
import logging.handlers
import json

class Log():
    "sys log class"

    logger = logging.getLogger(__name__)

    lock = threading.Lock()

    #flag=console log to console
    #flag=file log to file
    #flag=console&file log to console&file
    def Init(self, flag, loglevel):

        
        self.logger.setLevel(loglevel)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if flag == "console":
           console = logging.StreamHandler()
           console.setLevel(loglevel)
           self.logger.addHandler(console)
        if flag == "file":
           handler = logging.handlers.RotatingFileHandler("log.txt", maxBytes=1024*1024*10, backupCount=2)
           handler.setLevel(loglevel)
           handler.setFormatter(formatter)
           self.logger.addHandler(handler)
        if flag == "console&file":
           console = logging.StreamHandler()
           console.setLevel(loglevel)
           console.setFormatter(formatter)
           self.logger.addHandler(console)

           handler = logging.handlers.RotatingFileHandler("log.txt", maxBytes=1024*1024*10, backupCount=2)
           handler.setLevel(loglevel)
           handler.setFormatter(formatter)
           self.logger.addHandler(handler)

    def Fatal(self, msg):
        self.lock.acquire()
        self.logger.critical(msg)
        self.lock.release()

    def Error(self, msg):
        self.lock.acquire()
        self.logger.error(msg)
        self.lock.release()

    def Warning(self, msg):
        self.lock.acquire()
        self.logger.warning(msg)
        self.lock.release()

    def Info(self, msg):
        self.lock.acquire()
        self.logger.info(msg)
        self.lock.release()

    def Debug(self, msg):
        self.lock.acquire()
        self.logger.debug(msg)
        self.lock.release()

Log = Log()








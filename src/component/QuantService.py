# -*- coding: utf-8 -*-
import multiprocessing
from multiprocessing import Process, current_process, cpu_count, Manager
import zmq
from librabbitmq import Connection
import sys, os, time
import logging
import numpy as np
import copy
import datetime
import logging
from netifaces import ifaddresses

sys.path.append(os.environ['QUANT_HOME'] + '/lib')
sys.path.append(os.environ['QUANT_HOME'] + '/callback')

from CommonClass import Config
from DataCallBack import CallBack as DataCB
from StateCallBack import CallBack as StateCB
from ClassCallBack import CallBack as ClassCB
from Redis import RedisInfo
from Rabbitmq import RabbitMQClass

cfg = Config()
# current server ipaddress & process id
myaddress = eval(cfg.get('Server', 'ipaddress')) #ifaddresses('eth0')[2][0]['addr']
service = RedisInfo().get('service')[myaddress] #state, class, data
ppid = current_process()
pid_dir = cfg.get('Manager', 'pid_file')

# multiprocess message share
manager = Manager()
managerDict = manager.dict()
managerDict[0] = {'pid':ppid.pid, 'process_type':'parent', 'ipaddress':myaddress, 'service':service}
#manager process or parent pid
managerDict[1]= {'pid': 0}

# process pid info write

################################################################################
# @Date   : 2015-09-21 13:50
# @Version: 0.1
# @Author : jebuempak@gmail.com
# @Role   : QuantServer의 State Server를 담당
#           실행되는 Server의 IP Address로 Service 구분
# @Traget : Self Service
# @Method : MultiProcess로 구동
###############################################################################	
class StateService( RabbitMQClass, StateCB):
	def __init__(self, csGroup, routingKey, process_idle):
		RabbitMQClass.__init__(self)
		StateCB.__init__(self) #self.CallBack
		self.queueId  = routingKey
		self.routingKey= csGroup
		self.conn = None
		self.channel = None
		self.process_idle = process_idle

	def run(self):
		self.rabbitmq_connect()
		self.rabbitmq_channel()
		self.rabbitmq_consume(self.callback)
		self.rabbitmq_close()

	def callback(self, message):
		self._callback(message)
		
################################################################################
# @Date   : 2015-09-21 13:50
# @Version: 0.1
# @Author : jebuempak@gmail.com
# @Role   : QuantServer의 Class Server를 담당
#           실행되는 Server의 IP Address로 Service 구분
# @Traget : Self Service
# @Method : MultiProcess로 구동
###############################################################################	
class ClassService( RabbitMQClass, ClassCB ):
	def __init__(self, routingKey, process_idle):
		RabbitMQClass.__init__(self)
		ClassCB.__init__(self)
		self.queueId  = routingKey
		self.routingKey= routingKey
		self.conn = None
		self.channel = None
		self.process_idle = process_idle

	def run(self):
		self.rabbitmq_connect()
		self.rabbitmq_channel()
		self.rabbitmq_consume(self.callback)
		self.rabbitmq_close()

	def callback(self, message):
		self._callback(message)
		
################################################################################
# @Date   : 2015-09-21 13:50
# @Version: 0.1
# @Author : jebuempak@gmail.com
# @Role   : QuantServer의 Data Server를 담당
#           실행되는 Server의 IP Address로 Service 구분
# @Traget : Self Service
# @Method : MultiProcess로 구동
###############################################################################	
class DataService( RabbitMQClass, DataCB ):
	def __init__(self, csGroup, routingKey, process_idle):
		RabbitMQClass.__init__(self)
		DataCB.__init__(self)
		self.queueId  = csGroup
		self.routingKey= routingKey
		self.conn = None
		self.channel = None
		self.process_idle = process_idle

	def run(self):
		self.rabbitmq_connect()
		self.rabbitmq_channel()
		self.callback() #Data callback
		self.rabbitmq_close()

	def callback(self):
		self._callback()

# process pid를 list type으로 저장
def processWrite(pid):
	global pid_dir
	f = open(pid_dir, 'w')
	f.write(pid)
	f.close()

################################################################################
# @Date   : 2015-09-21 13:50
# @Version: 0.1
# @Author : jebuempak@gmail.com
# @Role   : QuantServer 상태 및 QuantManager client와 송수신 모듈
#           차후 Remote로 관리자가 설정할 수 있도록 하기 위함
# @Traget : Self Function
# @Method : MultiProcess로 구동
###############################################################################	
def processManager(host='0.0.0.0', port=5871):
	p = multiprocessing.current_process()
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://%s:%s" % (host, str(port) ) )
	while True:
		message = socket.recv()
		socket.send(str(managerDict))

def processStart(grp, rkey, serviceType='state'):
	p = multiprocessing.current_process()
	if serviceType == 'state':
		StateService(grp, rkey, p).run()
	elif serviceType == 'class':
		ClassService(grp, p).run()
	elif serviceType == 'data':
		DataService(grp, rkey, p).run()

def main():
	c = service
	s = RedisInfo().group_list()['state']
	n = 2
	p = multiprocessing.Process(target=processManager, args=('127.0.0.1', 5871,))
	p.start()
	managerDict[1]= {'pid': p.pid, 'process_type':'manager'}
	
	for x in s:
		try:
			p = multiprocessing.Process(target=processStart, args=(x, s[x], c,))
			p.start()
			argsText = '%s %s %s' % (x, s[x], c)
			managerDict[n] = {'pid':p.pid, 'process_type':'child', 'args':argsText}
			n = n + 1
		except KeyboardInterrupt:
			p.join()

	processWrite(str(managerDict))
	
if __name__ == '__main__':
	main()



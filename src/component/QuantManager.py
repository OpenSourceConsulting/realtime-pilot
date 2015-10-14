# -*- coding: utf-8 -*-
import multiprocessing
import zmq
#from zmq.utils.monitor import recv_monitor_message
#from multiprocessing import Process, current_process, cpu_count, Manager

import sys
import time, os
import socket
import psutil as ps

# virtual env setting
# os.environ['QUANT_HOME'] = '/home/quant'
sys.path.append(os.environ['QUANT_HOME'] + '/lib')
sys.path.append(os.environ['QUANT_HOME'] + '/cbc') # old callback => new cbc

from Redis import RedisInfo
from Rabbitmq import RabbitMQClass
import Daemon
import json
import math

from CommonClass import Config

# quant config text file read
cfg = Config()
pid_dir = cfg.get('Manager', 'pid_file')
manager_host = cfg.get('Manager', 'manager_host')
manager_port = int(cfg.get('Manager', 'manager_port'))

################################################################################
# @Author : jebuempak@gmail.com
# @Role   : pid_dir(/tmp/quantservice.pid)의 파일을 검사해서 Process의 살아나도록함
# @Traget : Self Service
# @Method : QuantManager.py client
###############################################################################	
class ProcessCheck(multiprocessing.Process):
	def __init__(self, pid_dir):
		multiprocessing.Process.__init__(self)
		self.pid_dir = pid_dir
		self.pid_dict = dict()

	def run(self):
		while True:
			self.check()
			time.sleep(1)

	def check(self):
		if os.path.exists(self.pid_dir) == True:
			self.pid_dict = eval(open(self.pid_dir, 'r').read())
			try:
				pid = int(self.pid_dict[0]['pid'])
				p = ps.Process(pid) #p.name(), p.cmdline()
				rst = True
			except:
				rst = False
		else:
			rst = False

		if rst == False:
			os.system( ("%s/bin/QuantService &") % (os.environ['QUANT_HOME']) )

################################################################################
# @Author : jebuempak@gmail.com
# @Role   : Process 감시 및 살아나도록 함, Process의 상태 정보를 송신 (live, defunc)
# @Traget : State, Class
# @Method : QuantManager.py client
# @Used   : Yes
###############################################################################	
class ProcessClient(object):
	def __init__(self, host='172.31.7.216', port=5871, pid_dir='/tmp/quantservice.pid'):
		self.context = zmq.Context(2) #.instance()
		#self.socket = self.context.socket(zmq.REQ)
		self.mananger_ip = host
		self.mananger_port = port
		self.mananger_socket = self.context.socket(zmq.REQ)
		self.mananger_socket.connect ("tcp://%s:%s" % (self.mananger_ip, self.mananger_port) )
		self.poll = zmq.Poller()
		self.poll.register(self.mananger_socket, zmq.POLLIN)
		self.request_timeout = 1000*60*60*24*365
		self.socks = None
		self.pid_dir = pid_dir
		self.pid_dict = dict()
		if os.path.exists(self.pid_dir) == True: self.pid_dict = eval(open(self.pid_dir, 'r').read())

	def run(self):
		#self.mananger_socket.setsockopt(zmq.LINGER, 0)
		while True:
			try:
				proc_dict = self.pid_dict
				for x in proc_dict:
					pid = int(proc_dict[x]['pid'])
					if x == 0: #parent
						p = ps.Process(pid) #p.name(), p.cmdline()
					else:
						p = ps.Process(pid)
					if [len(cmdline_list.strip()) for cmdline_list in p.cmdline()][0] == 0:
						proc_dict[x]['live'] = 'defunct'
					else:
						proc_dict[x]['live'] = 'live'
			except Exception, e:
				#print "Cleint Exception :", e
				proc_dict[x]['live'] = 'defunct'
			
			self.manager_send(str(proc_dict))
			time.sleep(1)

	def manager_send(self, m):
		try:
			self.mananger_socket.send (m)
			self.socks = dict(self.poll.poll(self.request_timeout))
			if self.socks.get(self.mananger_socket) == zmq.POLLIN:
				message = self.mananger_socket.recv()
				if not message:
					pass
					#break
				else:
					print message
			else:
				self.mananger_socket.setsockopt(zmq.LINGER, 0)
				self.mananger_socket.close()
				self.poll.unregister(self.mananger_socket)
				time.sleep(10)
				self.mananger_socket = self.context.socket(zmq.REQ)
				self.mananger_socket.connect ("tcp://%s:%s" % (self.mananger_ip, self.mananger_port) )
				self.poll.register(self.mananger_socket, zmq.POLLIN)
		except Exception, e:
			print e
			pass

################################################################################
# @Author : jebuempak@gmail.com
# @Role   : WebSocket
# @Traget : redis의 상태와 rabbitmq의 상태정보를 송신하는 WebSocket
# @Method : QuantManager.py server
# @Used   : Not
###############################################################################	
class MiddleWare(multiprocessing.Process, RabbitMQClass):
	def __init__(self):
		multiprocessing.Process.__init__(self)
		#RedisInfo.__init__(self)
		RabbitMQClass.__init__(self)
		
	def run(self):
		self.context = zmq.Context()
		self.websocket = self.context.socket(zmq.PUB)
		self.websocket.bind("tcp://127.0.0.1:10000")
		while True:
			j = dict()
			redis = self.redis_ping()
			rabbit= self.rabbitmq_ping()
			j['middleware'] = {'redis':redis, 'rabbitmq':rabbit}
			self.websocket.send( "%s" % ( json.dumps( j ) ) )

###############################################################################
# @Author : jebuempak@gmail.com
# @Role   : WebSocket
# @Traget : 각각의 Server의 Process Status를 송신해서 WebSocketServer 전달
# @Method : QuantManager.py server
# @Used   : Not
###############################################################################			
class ProcessManagerZeroMQ(object):
	def __init__(self, host='', port=5871):
		self.host = host
		self.port = port
		self.context = zmq.Context(10)
		self.socket = self.context.socket(zmq.REP)

		self.websocket = self.context.socket(zmq.PUB)
		self.websocket.bind("tcp://127.0.0.1:10005")
    
	def start(self):
		self.socket.bind("tcp://%s:%s" % (self.host, str(self.port) ) )
		while True:
			j = dict()
			message = self.socket.recv()
			j['process'] = eval(message)
			self.websocket.send( "%s" % ( json.dumps( j ) ) ) #str(json.dumps(dict(x=x, y=y)))) )
			self.socket.send("OK")
			time.sleep(1)

##############################################################################
# @Author : jebuempak@gmail.com
# @Role   : WebSocket
# @Traget : 각각의 Server의 Process Status를 송신해서 WebSocketServer 전달
# @Method : QuantManager.py server
# @Used   : Yes
###############################################################################			
class ProcessManager(object, RabbitMQClass):
	def __init__(self, host='', port=5871):
		RabbitMQClass.__init__(self)
		self.host = host
		self.port = port
		self.context = zmq.Context(20)
		self.socket = self.context.socket(zmq.REP)

	def start(self):
		self.socket.bind("tcp://%s:%s" % (self.host, str(self.port) ) )
		sequence = 0
		while True:
			sequence += 1
			message = self.socket.recv()
			try:
				j = dict()
				############ service server state #############
				j['process'] = eval(message)
				############ redis, rabbitmq state ############
				redis = self.redis_ping()
				rabbit= self.rabbitmq_ping()
				j['middleware'] = {'redis':redis, 'rabbitmq':rabbit}
				self.master_publish( 'service_state', json.dumps( j ) )
				self.socket.send(str(sequence) + " OK")
			except Exception, e:
				print "Manager Exception :", e, message
				self.socket.send(message)
				pass
			#time.sleep(0.1)

##############################################################################
# @Author : jebuempak@gmail.com
# @Role   : QuantManager Stop
# @Traget : Self
# @Method : QuantManager.py stop
# @Used   : Yes
###############################################################################			

#################################################################################
# ProcessClient에 Object 상속에 multiprocessing.Process를 상속하지 않는 이유는 ZeroMQ와 충돌함
# ###############################################################################
def defProcessClient(host='172.31.7.216', port=5871, pid_dir='/tmp/quantservice.pid'):
	ProcessClient(host='172.31.7.216', port=5871, pid_dir='/tmp/quantservice.pid').run()

def processCheck(host=manager_host, port=5871, pid_dir='/tmp/quantservice.pid'):
	ProcessCheck(pid_dir).start()
	time.sleep(1)
	multiprocessing.Process(target=defProcessClient, args=(manager_host, manager_port, pid_dir,)).start()

def managerstop():
	pid = open('/tmp/quantmanager.pid','r').read()
	try:
		p = ps.Process(int(pid))
		p.terminate()
		time.sleep(1)
	except: pass

	try:
		for x in ps.pids():
			p = ps.Process(x)
			if 'QuantManager' in str(p.cmdline()):
				#print x, p.cmdline()
				p.terminate()
	except: pass

if __name__ == '__main__':
	if sys.argv[1] == 'stop':
		managerstop()
		exit()
	Daemon.Daemon(pidfile='/tmp/quantmanager.pid').runAsDaemon()
	if sys.argv[1] == 'server':
		ProcessManager(host='0.0.0.0', port=manager_port).start()
	elif sys.argv[1] == 'client':
		processCheck(host='127.0.0.1', port=manager_port)
	
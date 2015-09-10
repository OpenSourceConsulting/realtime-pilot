# -*- coding: utf-8 -*-
import zmq
from zmq.utils.monitor import recv_monitor_message
import threading
import sys
import time, os
import socket
import psutil as ps
sys.path.append(os.environ['QUANT_HOME'] + '/lib')
import Daemon
import json
import math

class ProcessCheck(object):
	def __init__(self, host='127.0.0.1', port=5871):
			self.host = host
			self.port = port
			self.context = zmq.Context.instance()
			self.socket = self.context.socket(zmq.REQ)
			#self.socket.connect ("tcp://%s:%s" % (self.host, self.port) )

			self.mananger_ip='172.31.7.216'
			self.mananger_port=5871
			self.mananger_socket = self.context.socket(zmq.REQ)
			self.mananger_socket.connect ("tcp://%s:%s" % (self.mananger_ip, self.mananger_port) )

	def start(self):
		self.socket.connect ("tcp://%s:%s" % (self.host, self.port) )
		while True:
			self.socket.send ('process check request')
			message = self.socket.recv()
			while True:
				try:
					d = eval(message)
					for x in d:
						if x == 0:
							proc_num = int(d[x]['pid'])
							print proc_num
							p = ps.Process(proc_num) #p.name(), p.cmdline()
						else:
							p = ps.Process(x)
						
						if [len(cmdline_list.strip()) for cmdline_list in p.cmdline()][0] == 0: d[x]['live'] = 'defunct'
					print d
					self.manager_send(str(d))
				except Exception, e:
					print "Exception :", e
					self.manager_send(str(d))
					return False
				time.sleep(1)

	def manager_send(self, m):
		self.mananger_socket.send (m)
		message = self.mananger_socket.recv()
		print message

class MessageServer(object):
	def __init__(self, host='', port=5872):
		self.host = host
		self.port = port
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)
		
		self.websocket = self.context.socket(zmq.PUB)
		self.websocket.bind("tcp://127.0.0.1:5001")
    
	def start(self):
		self.socket.bind("tcp://%s:%s" % (self.host, str(self.port) ) )
		while True:
			message = self.socket.recv()
			print "Message ======================================>"
			print message
			self.websocket.send( "%s" % (message) ) #str(json.dumps(dict(x=x, y=y)))) )
			self.socket.send("OK")
			print "Message ======================================>"
			print

class ProcessManager(object):
	def __init__(self, host='', port=5871):
		self.host = host
		self.port = port
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)

		self.websocket = self.context.socket(zmq.PUB)
		self.websocket.bind("tcp://127.0.0.1:5000")
    
	def start(self):
		self.socket.bind("tcp://%s:%s" % (self.host, str(self.port) ) )
		while True:
			message = self.socket.recv()
			print message
			x = time.time()
			y = 2.5 * (1 + math.sin(x))
			self.websocket.send( "%s" % (message) ) #str(json.dumps(dict(x=x, y=y)))) )
			self.socket.send("OK")

def processCheck(host='127.0.0.1', port=5871):
	while True:
		z = ProcessCheck(host='127.0.0.1', port=5871).start()
		if z == False:
			#os.system("/home/ec2-user/source/Quant/QuantService &")
			time.sleep(30)

if __name__ == '__main__':
	#Daemon.Daemon(pidfile='/tmp/qauntmanager.pid').runAsDaemon()
	if sys.argv[1] == 'server':
		ProcessManager(host='0.0.0.0', port=5871).start()
	elif sys.argv[1] == 'client':
		processCheck(host='127.0.0.1', port=5871)
	elif sys.argv[1] == 'message':
		MessageServer(host='0.0.0.0', port=5872).start()
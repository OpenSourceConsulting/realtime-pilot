import zmq
from zmq.utils.monitor import recv_monitor_message
import threading
import sys
import time, os
import psutil as ps

class ProcessCheck(object):
	def __init__(self, host='127.0.0.1', port=5871):
			self.host = host
			self.port = port
			self.context = zmq.Context()
			self.socket = self.context.socket(zmq.REQ)
			self.EVENT_MAP = {}

	def start(self):
		self.socket.connect ("tcp://%s:%s" % (self.host, self.port) )
		while True:
			self.socket.send ('process check request')
			message = self.socket.recv()
			while True:
				try:
					d = eval(message)
					for x in d:
						p = ps.Process(x)
						if len(p.cmdline()) == 1: d[x]['live'] = 'defunct'
					print d
				except:
					return False
					break
				time.sleep(1)
			
while True:
	z = ProcessCheck(host='127.0.0.1', port=5871).start()
	if z == False:
		os.system("python /home/ec2-user/source/Quant/QuantService.py state &")
		time.sleep(1)
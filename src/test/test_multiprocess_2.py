"""
from multiprocessing.managers import BaseManager
import time
import psutil as ps
class QueueManager(BaseManager): pass
QueueManager.register('get_queue')
m = QueueManager(address=('127.0.0.1', 50000), authkey='quant1234')
m.connect()
queue = m.get_queue()

while True:
	try:
		g = queue.get()

		p = ps.Process(x)
				if len(p.cmdline()) == 1:
					d[x]['live'] = 'defunct'
		
		print g
	except:
		print "Process Down"
		queue = m.get_queue()

	time.sleep(1)
"""

import zmq
import sys
import time
import psutil as ps

class Zeromq(object):
	def __init__(self, host='', port=5000):
		self.host = host
		self.port = port
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)

	def start(self):
		self.socket.bind("tcp://%s:%s" % (self.host, str(self.port) ) )
		while True:
			message = self.socket.recv()
			
			d = eval(message)
			for x in d:
				p = ps.Process(x)
				if len(p.cmdline()) == 1: d[x]['live'] = 'defunct'
			print d
			
			self.socket.send('Thank You')


z = Zeromq(host='127.0.0.1', port=5000)
z.start()
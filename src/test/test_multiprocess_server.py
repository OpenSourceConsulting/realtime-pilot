from multiprocessing import Process, current_process, cpu_count, Manager

import time, os
import psutil as ps
import copy
import zmq


class Worker(Process):
	def __init__(self):
		super(Worker, self).__init__()
	def run(self):
		while True:
			l[self.pid] = {'pid_type':'child', 'live': self.is_alive()}
			time.sleep(1)

class ProcessManager(object):
	def __init__(self, host='', port=5871):
		self.host = host
		self.port = port
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)

	def start(self):
		self.socket.bind("tcp://%s:%s" % (self.host, str(self.port) ) )
		while True:
			message = self.socket.recv()
			#print message
			self.socket.send(str(l))

def zmqClient():
	port = "5000"
	context = zmq.Context()
	print "Connecting to server..."
	socket = context.socket(zmq.REQ)
	socket.connect ("tcp://localhost:%s" % port)

	while True:
		print "Process Status ..."

		socket.send (str(l))
		#  Get the reply.
		message = socket.recv()
		print "Process Statue : [", message, "]"
		time.sleep(1)


if __name__ == '__main__':
	#main()
	#l = dict()
	ppid = current_process()
	manager = Manager()
	l = manager.dict()

	l[ppid.pid] = {'pid_type':'parent', 'live':ppid.is_alive()}
	"""
	for x in [0, 1, 2]:
		w = Worker()
		w.start()
		l[w.pid] = {'pid_type':'child', 'live': w.is_alive()}
	"""
	ProcessManager(host='0.0.0.0', port=5871).start()

	
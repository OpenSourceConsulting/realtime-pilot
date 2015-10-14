import time, os
import psutil as ps
import copy
import zmq


class Zeromq(object):
	def __init__(self, l, host='', port=5000):
		self.host = host
		self.port = port
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)

	def start(self):
		self.socket.bind("tcp://%s:%s" % (self.host, str(self.port) ) )
		while True:
		    #  Wait for next request from client
		    message = self.socket.recv()
		    time.sleep (1)  
		    self.socket.send("World from %s" % self.port)


if __name__ == '__main__':
	l = dict()
	z = Zeromq(l, host='0.0.0.0', port=5000)
	z.start()

	
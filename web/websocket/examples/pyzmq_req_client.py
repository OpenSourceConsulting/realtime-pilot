

import time
import gevent.monkey
gevent.monkey.patch_all()
from gevent_zeromq import zmq
import gevent

c = zmq.Context()
s = c.socket(zmq.REQ)
s.connect('tcp://127.0.0.1:10004')

n = 0
while True:
	t = 'sending %d' % n
	s.send(str(t))
	print t
	print s.recv();
	time.sleep(1)
	n = n + 1

	"""
	for c  in  range(100):
		print 'sending %s' % c
		s.send(str(c))
		print s.recv();
		time.sleep(1)
	"""

    

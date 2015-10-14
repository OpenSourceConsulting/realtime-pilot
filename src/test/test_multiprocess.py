from multiprocessing import Process, current_process, cpu_count
import time
#print cpu_count(), 


def test(text):
	#while True:
	#	print text
	#	time.sleep(1)
	return text

def main():
	l = {}
	m = current_process().pid
	l[m] = list()
	for x in range(3):
		p = Process(target=test, args=('test',))
		p.start()
		#l[m].append(p.pid)
		l[m].append(p.pid)
		print p, p.pid, p.is_alive()

	print "Process PID :", l

if __name__ == '__main__':
	main()
	time.sleep(3600)

"""
from multiprocessing.managers import BaseManager
import Queue
queue = Queue.Queue()
class QueueManager(BaseManager): pass

def getQueue():
	print 
	return queue

QueueManager.register('get_queue', callable=lambda: queue)
m = QueueManager(address=('', 50000), authkey='abracadabra')
s = m.get_server()
s.serve_forever()
"""
"""
from multiprocessing import Process, Queue
from multiprocessing.managers import BaseManager

class Worker(Process):
	def __init__(self, q):
		self.q = q
		super(Worker, self).__init__()
	def run(self):
		self.q.put('local hello')

queue = Queue()
w = Worker(queue)
w.start()
class QueueManager(BaseManager): pass

QueueManager.register('get_queue', callable=lambda: queue)
m = QueueManager(address=('', 50000), authkey='abracadabra')
s = m.get_server()
s.serve_forever()
"""










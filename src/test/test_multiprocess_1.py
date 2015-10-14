from multiprocessing.managers import BaseManager
import time
class QueueManager(BaseManager): pass
QueueManager.register('get_queue')
m = QueueManager(address=('127.0.0.1', 50000), authkey='quant1234')
m.connect()
queue = m.get_queue()
while True:
	queue.put('Proecess Down')
	print queue.get(), 1
	time.sleep(1)
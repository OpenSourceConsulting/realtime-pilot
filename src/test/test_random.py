import sys, os, time
import logging
import numpy as np
import copy
import time


sys.path.append(os.environ['QUANT_HOME'] + '/lib')
sys.path.append(os.environ['QUANT_HOME'] + '/callback')
from StateCallBack import CallBack as StateCB
from ClassCallBack import CallBack as ClassCB
from Redis import RedisInfo 

global_group = None

class RabbitMQClass(RedisInfo, StateCB ):
	def __init__(self):
		RedisInfo.__init__(self)
		StateCB.__init__(self) #self.callback
		self.rabbitmq = self.rabbitmq()
		self.new_rabbitmq = copy.deepcopy(self.rabbitmq.keys())
		self.rabbitmq_cluster = 0
		
	def cluster_random(self):
		while True:
			self.rabbitmq_cluster = np.random.randint(2)
			print self.rabbitmq_cluster,
			self.new_rabbitmq = copy.deepcopy(self.rabbitmq.keys())
			self.new_rabbitmq.remove(self.rabbitmq_cluster)
			self.rabbitmq_cluster = np.random.choice(self.new_rabbitmq, 1)[0]
			print self.rabbitmq[self.rabbitmq_cluster]
			time.sleep(5)


r = RabbitMQClass()
r.cluster_random()
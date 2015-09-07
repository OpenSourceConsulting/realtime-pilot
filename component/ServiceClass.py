# -*- coding: utf-8 -*-
import multiprocessing
from multiprocessing import Process, current_process, cpu_count, Manager
import zmq
from librabbitmq import Connection
import sys, os, time
import logging
import numpy as np
import copy
import logging

#import Daemon
#import daemon
#from daemon import runner

sys.path.append(os.environ['QUANT_HOME'] + '/lib')
sys.path.append(os.environ['QUANT_HOME'] + '/callback')
from DataCallBack import CallBack as DataCB
from StateCallBack import CallBack as StateCB
from ClassCallBack import CallBack as ClassCB
from Redis import RedisInfo 

ppid = current_process()
manager = Manager()
managerDict = manager.dict()
managerDict[ppid.pid] = {'pid_type':'parent', 'live':ppid.is_alive()}

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
			self.socket.send(str(managerDict))

class RabbitMQClass( RedisInfo ):
	def __init__(self):
		RedisInfo.__init__(self)
		self.rabbitmq = self.rabbitmq()
		self.new_rabbitmq = copy.deepcopy(self.rabbitmq.keys())
		self.rabbitmq_cluster = 0
		self.hostname = self.rabbitmq[self.rabbitmq_cluster]['hostname']
		self.port = int(self.rabbitmq[self.rabbitmq_cluster]['port'])
		self.user = self.rabbitmq[self.rabbitmq_cluster]['user']
		self.password = self.rabbitmq[self.rabbitmq_cluster]['pass']
		self.vhost = self.rabbitmq[self.rabbitmq_cluster]['vhost']
		self.exchange_name = self.rabbitmq[self.rabbitmq_cluster]['exchange_name']
		#self.queueId = "quantq"
		
	def cluster_random(self):
		self.new_rabbitmq = copy.deepcopy(self.rabbitmq.keys())
		self.new_rabbitmq.remove(self.rabbitmq_cluster)
		self.rabbitmq_cluster = np.random.choice(self.new_rabbitmq, 1)[0]
		self.hostname = self.rabbitmq[self.rabbitmq_cluster]['hostname']
		self.port = int(self.rabbitmq[self.rabbitmq_cluster]['port'])
		self.user = self.rabbitmq[self.rabbitmq_cluster]['user']
		self.password = self.rabbitmq[self.rabbitmq_cluster]['pass']
		self.vhost = self.rabbitmq[self.rabbitmq_cluster]['vhost']
		self.exchange_name = self.rabbitmq[self.rabbitmq_cluster]['exchange_name']

	def rabbitmq_connect(self):
		try:
			#print "Test1", self.rabbitmq_cluster, self.hostname, self.port
			self.conn = Connection(host=self.hostname, port=self.port, userid=self.user, password=self.password, virtual_host=self.vhost)
			connect_check = 'True' if self.conn else 'False'
		except Exception, e:
			self.cluster_random()
			self.conn = Connection(host=self.hostname, port=self.port, userid=self.user, password=self.password, virtual_host=self.vhost)
			connect_check = 'True' if self.conn else 'False'

	def rabbitmq_channel(self):
		self.channel = self.conn.channel()
		#self.channel.exchange_declare(self.exchange_name, type='direct',  passive=True, durable=True, auto_delete=False, arguments=None, nowait=False)
		#self.queueId = self.channel.queue_declare( exclusive=True, durable =True, auto_delete=False ).queue
		#self.channel.queue_bind(self.queueId, self.exchange_name, self.routingKey)
		self.channel.exchange_declare( self.exchange_name, type='direct',  durable=True)
		self.channel.queue_declare( self.queueId, exclusive=False, durable =True )
		#self.channel.queue_bind(self.queueId, self.exchange_name, self.routingKey)


	def rabbitmq_publish(self, callback=None):
		
		try:
			message = callback
			self.channel.basic_publish(message, '', self.routingKey)
		except:
			self.rabbitmq_connect()
			self.rabbitmq_channel()
			self.channel.basic_publish(message, '', self.routingKey)

	def rabbitmq_consume(self):
		try:
			self.channel.basic_consume(self.queueId, callback=self.callback)
		except KeyboardInterrupt:
			self.channel.close()
			self.conn.close()

		while True:
			try:
				self.conn.drain_events()
			except Exception, e:
				self.rabbitmq_connect()
				self.rabbitmq_channel()
				self.rabbitmq_consume()

	def rabbitmq_close(self):
		try:
			pass
		except KeyboardInterrupt:
			self.channel.close()
			self.conn.close()


class StateService( RabbitMQClass, StateCB ):
	def __init__(self, csGroup, routingKey, process_idle):
		RabbitMQClass.__init__(self)
		StateCB.__init__(self) #self.callback
		self.queueId  = routingKey
		self.routingKey= csGroup
		self.conn = None
		self.channel = None
		self.process_idle = process_idle

	def run(self):
		self.rabbitmq_connect()
		self.rabbitmq_channel()
		self.rabbitmq_consume()
		self.rabbitmq_close()

	def callback(self, message):
		self._callback(message)


class ClassService( RabbitMQClass, ClassCB ):
	def __init__(self, routingKey, process_idle):
		RabbitMQClass.__init__(self)
		ClassCB.__init__(self)
		self.queueId  = routingKey
		self.routingKey= routingKey
		self.conn = None
		self.channel = None
		self.process_idle = process_idle

	def run(self):
		self.rabbitmq_connect()
		self.rabbitmq_channel()
		self.rabbitmq_consume()
		self.rabbitmq_close()

	def callback(self, message):
		#print("Body:'%s', Proeprties:'%s', DeliveryInfo:'%s'" % ( message.body, message.properties, message.delivery_info))
		self._callback(message)
		#message.ack()
		#channel.basic_publish(message.body, exchange_name, arg_rky)


class DataService( RabbitMQClass, DataCB ):
	def __init__(self, routingKey, process_idle):
		RabbitMQClass.__init__(self)
		DataCB.__init__(self)
		self.routingKey= routingKey
		self.conn = None
		self.channel = None
		self.process_idle = process_idle

	def run(self):
		self.rabbitmq_connect()
		self.rabbitmq_channel()
		self.rabbitmq_publish(self.callback)
		self.rabbitmq_close()

	@property
	def callback(self):
		#self.channel.basic_publish(arg_body.replace("KR", x), exchange_name, arg_rky)
		#print("Body:'%s', Proeprties:'%s', DeliveryInfo:'%s'" % ( message.body, message.properties, message.delivery_info))
		self._callback()
		#message.ack()
		#channel.basic_publish(message.body, exchange_name, arg_rky)

def processStart(grp, rkey, serviceType='state'):
	p = multiprocessing.current_process()
	if serviceType == 'state':
		StateService(grp, rkey, p).run()
	elif serviceType == 'class':
		ClassService(grp, p).run()
	elif serviceType == 'data':
		DataService(rkey, p).run()

def main(c):

	s = RedisInfo().group_list()['state']
	for x in s:
		try:
			p = multiprocessing.Process(target=processStart, args=(x, s[x], c,))
			#p.daemon = True
			p.start()
			managerDict[p.pid] = {'pid_type':'child', 'live': p.is_alive()}
		except KeyboardInterrupt:
			p.join()

	ProcessManager(host='0.0.0', port=5871).start()
	
if __name__ == '__main__':
	#PIDFILE = '/tmp/quant.pid'
	#Daemon.Daemon(pidfile = PIDFILE).runAsDaemon()
	#with daemon.DaemonContext():
	main(sys.argv[1])
	
	"""
	logger = logging.getLogger("DaemonLog")
	logger.setLevel(logging.INFO)
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	handler = logging.FileHandler("/var/log/quant/quant.log")
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	"""
	#daemon_runner = runner.DaemonRunner(app)
	##daemon_runner.daemon_context.files_preserve=[handler.stream]
	#daemon_runner.do_action()
	



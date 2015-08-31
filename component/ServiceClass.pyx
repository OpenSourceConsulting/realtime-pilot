import multiprocessing
from librabbitmq import Connection
import sys, os
sys.path.append(os.environ['QUANT_HOME'] + '/lib')
sys.path.append(os.environ['QUANT_HOME'] + '/callback')
import StateCallBack
import ClassCallBack

import rdm

r = rdm.RedisInfo()
hostname = r.rmq['hostname']
port = r.rmq['port']
user = r.rmq['user']
password = r.rmq['pass']
vhost = r.rmq['vhost']
exchange_name = 'quant'

#arg_que = 'AADD' #sys.argv[2]
#arg_rky = sys.argv[1]
#arg_body = sys.argv[2]

class StateService(object, StateCallBack.CallBack):
	def __init__(self, csGroup, routingKey, process_idle):
		self.csGroup = csGroup
		self.routingKey= routingKey
		self.conn = None
		self.channel = None
		self.exchange_name = exchange_name
		self.process_idle = process_idle

	def run(self):
		#arg_nam = sys.argv[1]
		#arg_rky = sys.argv[2]
		#arg_body = sys.argv[2]
		self.conn = Connection(host=hostname, port=port, userid=user, password=password, virtual_host=vhost)
		self.channel = self.conn.channel()
		self.channel.exchange_declare(exchange_name, 'topic')
		queueId = self.channel.queue_declare( exclusive = True ).queue
		self.channel.queue_bind(queueId, exchange_name, self.routingKey)
		self.channel.basic_consume(queueId, callback=self.callback)
        
		"""
		try:
			self.channel.basic_consume(queueId, callback=self.callback)
		except KeyboardInterrupt:
			self.channel.close()
		self.conn.close()
		"""
		while True:
			self.conn.drain_events()

	def callback(self, message):
		#print("Body:'%s', Proeprties:'%s', DeliveryInfo:'%s'" % ( message.body, message.properties, message.delivery_info))
		self._callback(message)
		#print message.body

		#self.channel.basic_publish(message.body, exchange_name, self.csGroup)
		#message.ack()
		#message.reject()

	def close(self):
		self.conn.close()

class ClassService(object, ClassCallBack.CallBack):
	def __init__(self, routingKey, process_idle):
		self.routingKey= routingKey
		self.conn = None
		self.channel = None
		self.process_idle = process_idle

	def run(self):
		self.conn = Connection(host=hostname, port=port, userid=user, password=password, virtual_host=vhost)
		self.channel = self.conn.channel()
		self.channel.exchange_declare(exchange_name, 'topic')
		queueId = self.channel.queue_declare( exclusive = True ).queue
		self.channel.queue_bind(queueId, exchange_name, self.routingKey)
		
		try:
			self.channel.basic_consume(queueId, callback=self.callback)
		except KeyboardInterrupt:
			self.channel.close()
			self.conn.close()

		while True:
			self.conn.drain_events()

	def callback(self, message):
		#print("Body:'%s', Proeprties:'%s', DeliveryInfo:'%s'" % ( message.body, message.properties, message.delivery_info))
		#print message.body
		self._callback(message)
		#message.ack()
		#channel.basic_publish(message.body, exchange_name, arg_rky)

	def close(self):
		self.conn.close()

def processStart(grp, rkey, classType='state'):
	p = multiprocessing.current_process()
	if classType == 'state':
		StateService(grp, rkey, p).run()
	elif classType == 'class':
		ClassService(rkey, p).run()

def main(c):
	s = r.grp['state']
	for x in s:
		p = multiprocessing.Process(target=processStart, args=(x, s[x], c,)).start()
	
if __name__ == '__main__':
	main(sys.argv[1])
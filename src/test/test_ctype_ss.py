import multiprocessing as mp
from multiprocessing import Process
from multiprocessing import Pool
from librabbitmq import Connection
import sys
sys.path.append("/home/ec2-user/source/Quant/component")
from optparse import OptionParser as parser

import rdm

r = rdm.RedisInfo()
hostname = r.rmq['hostname']
port = r.rmq['port']
user = r.rmq['user']
password = r.rmq['pass']
vhost = r.rmq['vhost']
exchange_name = 'quant'


class StateService(object):
	def __init__(self, csGroup, routingKey):
		self.csGroup = csGroup
		self.routingKey= routingKey
		self.conn = None
		self.channel = None

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
		print message.body
		self.channel.basic_publish(message.body, exchange_name, self.csGroup)
		#message.ack()
		#message.reject()


	def close(self):
		self.conn.close()

def processStart(grp, rkey):
	StateService(grp, rkey).run()

if __name__ == '__main__':
	s = r.grp['state']
	for x in s:
		p = Process(target=processStart, args=(x, s[x],)).start()
    	#p.join()
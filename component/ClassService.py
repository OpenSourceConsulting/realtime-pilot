import multiprocessing as mp
from multiprocessing import Process
from multiprocessing import Pool
from librabbitmq import Connection
import sys
sys.path.append("/home/ec2-user/source/Quant/component")

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

class ClassService(object):
	def __init__(self, routingKey):
		self.routingKey= routingKey
		self.conn = None
		self.channel = None

	def run(self):
		self.conn = Connection(host=hostname, port=port, userid=user, password=password, virtual_host=vhost)
		self.channel = self.conn.channel()
		self.channel.exchange_declare(exchange_name, 'topic')
		queueId = self.channel.queue_declare( exclusive = True ).queue
		self.channel.queue_bind(queueId, exchange_name, self.routingKey)
		try:
		    self.channel.basic_consume(queueId, callback=self.callback_rdm)
		except KeyboardInterrupt:
		    self.channel.close()
		    self.conn.close()

		while True:
			self.conn.drain_events()


	def callback_rdm(self, message):
			#print("Body:'%s', Proeprties:'%s', DeliveryInfo:'%s'" % ( message.body, message.properties, message.delivery_info))
			print "Class =====> ", message.body
			#message.ack()
			#channel.basic_publish(message.body, exchange_name, arg_rky)

	def close(self):
		self.conn.close()

def processStart(rkey):
	ClassService(rkey).run()

if __name__ == '__main__':
	s = r.grp['state']
	for x in s:
		p = Process(target=processStart, args=(x,)).start()
    	#p.join()
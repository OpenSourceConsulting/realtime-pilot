

#!/usr/bin/env python
import sys
import pika

sys.path.append("/home/ec2-user/source/Quant/component")

import rdm
r = rdm.RedisInfo()

arg_exchange = sys.argv[1]
arg_queue    = sys.argv[2]
arg_routing_key=sys.argv[3]

credentials = pika.PlainCredentials( r.rmq['user'], r.rmq['pass'] )
parameters = pika.ConnectionParameters( r.rmq['hostname'], r.rmq['port'], 'dev-quant-1', credentials )
connection = pika.BlockingConnection( parameters )

channel = connection.channel(2)

channel.exchange_declare( exchange = arg_exchange, type='direct' )
channel.queue_declare(queue=arg_queue)
#channel.queue_declare( exclusive = True )
channel.queue_bind( exchange = arg_exchange, queue = arg_queue, routing_key = arg_routing_key )

while True:
	s = raw_input("Body : ")
	if s == 'exit':
		connection.close()
		exit()
	#channel.queue_bind( exchange = 'topic_logs', queue = self._queueID, routing_key = topic )
	channel.basic_publish(exchange = arg_exchange,
		              #queue=arg_queue,
                      routing_key=arg_routing_key,
                      body=s)
	print " [x] Sent '%s'" % s
connection.close()
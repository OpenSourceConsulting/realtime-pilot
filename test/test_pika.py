

#!/usr/bin/env python
import sys
import pika

sys.path.append("/home/ec2-user/source/Quant/component")

import rdm
r = rdm.RedisInfo()

arg_exchange = sys.argv[1]
arg_queue    = sys.argv[2]
#arg_routing_key=sys.argv[3]
msg = sys.argv[3]

def on_connection_open():
	pass

credentials = pika.PlainCredentials( r.rmq['user'], r.rmq['pass'] )
parameters = pika.ConnectionParameters( r.rmq['hostname'], r.rmq['port'], r.rmq['vhost'], credentials )
#connection = pika.BlockingConnection( parameters )
connection = pika.AsyncoreConnection(parameters, on_open_callback=callback)

channel = connection.channel()
channel.exchange_declare( exchange = arg_exchange, type='topic' )
routingKey=arg_queue


#message = raw_input("Message : ")
channel.basic_publish(exchange = arg_exchange,
		              #queue=arg_queue,
                      routing_key=routingKey,
                      body=msg)
connection.close()
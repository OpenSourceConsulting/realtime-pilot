#!/usr/bin/env python
import sys
sys.path.append("/home/ec2-user/source/Quant/component")

import rdm
import pika

r = rdm.RedisInfo()

arg_exchange    = sys.argv[1]
arg_queue       = sys.argv[2]
#arg_routing_key = sys.argv[3]
try:arg_vhost=sys.argv[3]
except:arg_vhost=None

credentials = pika.PlainCredentials( r.rmq['user'], r.rmq['pass'] )

if arg_vhost != None:
	r.rmq['vhost'] = arg_vhost

parameters = pika.ConnectionParameters( r.rmq['hostname'], r.rmq['port'], r.rmq['vhost'], credentials )

connection = pika.BlockingConnection( parameters )
channel = connection.channel()

#channel.exchange_declare( exchange = arg_exchange, type='topic' )
#queueID = channel.queue_declare( exclusive = True ).method.queue

channel.exchange_declare( exchange = arg_exchange, type = 'topic' )
queueId = channel.queue_declare( exclusive = True ).method.queue
channel.queue_bind(exchange = arg_exchange, queue = queueId, routing_key = arg_queue )

#channel.queue_bind( exchange = arg_exchange, queue = queueID, routing_key = arg_queue)

def on_message(channel, method, header, b):
    #print method
    print "rounting_key :", method.routing_key
    print "body         :", b


channel.basic_consume(on_message, queue=queueId, no_ack = True)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    
connection.close()
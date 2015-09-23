#!/usr/bin/env python
import sys
sys.path.append("/home/ec2-user/source/Quant/component")

import rdm
import pika

r = rdm.RedisInfo()

arg_exchange    = sys.argv[1]
arg_queue       = sys.argv[2]
arg_routing_key = sys.argv[3]
#try:arg_vhost=sys.argv[4]
#except:arg_vhost=None

credentials = pika.PlainCredentials( r.rmq['user'], r.rmq['pass'] )

#if arg_vhost != None:
#	r.rmq['vhost'] = arg_vhost

parameters = pika.ConnectionParameters( r.rmq['hostname'], r.rmq['port'], r.rmq['vhost'], credentials )

connection = pika.BlockingConnection( parameters )
#connection = pika.AsyncoreConnection( parameters, stop_ioloop_on_close=False )
channel = connection.channel()
channel.exchange_declare( exchange = arg_exchange, type='topic' )
queueID = channel.queue_declare( exclusive = True ).method.queue
channel.queue_bind( exchange = arg_exchange, queue = queueID, routing_key = arg_routing_key)


def on_message(channel, method, header, b):
	print "rounting_key(Send Queue) :", method.routing_key, method
	print "body         :", b
	print "arg_queue :", arg_exchange, arg_queue
	channel.basic_publish( exchange = arg_exchange, routing_key=arg_queue, body=b)

channel.basic_consume(on_message, queue=queueID, no_ack = True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    connection.close()
connection.close()
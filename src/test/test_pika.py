#!/usr/bin/env python
import pika
import sys, os

import time

sys.path.append(os.environ['QUANT_HOME'] + '/lib')
from Redis import RedisInfo

r = RedisInfo()
rabbitmq_cluster = 0
hostname, port, user, password, vhost, exchange_name, rabbitmq_number = r.rabbitmq(rabbitmq_cluster)


credentials = pika.PlainCredentials( user, password )
parameters = pika.ConnectionParameters( hostname, port, vhost, credentials )
connection = pika.BlockingConnection( parameters )

channel = connection.channel()

channel.exchange_declare( exchange = exchange_name, type='direct', durable=True)
#channel.queue_declare(queue='task_queue', durable=True)

n = 0
while True:
	message = "Rabbitmq Test 12345678 %d" % n

	channel.basic_publish(exchange='',
	                      routing_key='XKRX-CS-KR',
	                      body=message)
	"""
	channel.basic_publish(exchange='',
	                      routing_key='task_queue',
	                      body=message),
	                      properties=pika.BasicProperties(
	                         delivery_mode = 2, # make message persistent
	                      ))
	"""

	print " [x] Sent %r" % (message,)
	n = n + 1
	time.sleep(1)

connection.close()

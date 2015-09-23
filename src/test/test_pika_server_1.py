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

channel.exchange_declare( exchange = exchange_name, type='direct' , durable=True)
channel.queue_declare(queue='task_queue_1', durable=True)
print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    #time.sleep( body.count('.') )
    print " [x] Done"
    #ch.basic_ack(delivery_tag = method.delivery_tag)

#channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue_1')
channel.start_consuming()
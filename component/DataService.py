from librabbitmq import Connection
import time
import sys, os
sys.path.append(os.environ['QUANT_HOME'] + '/lib')
from Redis import RedisInfo
import uuid

def Connect():
	r = RedisInfo()
	rabbitmq_cluster = 0
	hostname, port, user, password, vhost, exchange_name, rabbitmq_number = r.rabbitmq(rabbitmq_cluster)
	
	try:
		conn = Connection(host=hostname, port=port, userid=user, password=password, virtual_host=vhost)
	except Exception, e:
		print "Exception :", e
		rabbitmq_cluster = 1
		hostname, port, user, password, vhost, exchange_name, rabbitmq_number = r.rabbitmq(rabbitmq_cluster)
		print hostname, port
		conn = Connection(host=hostname, port=port, userid=user, password=password, virtual_host=vhost)


	#queueId = "quantq"
	channel = conn.channel()
	channel.exchange_declare(exchange_name, type='direct', durable=True, )

	#channel.queue_declare( 'bloom', exclusive=True, auto_delete=False, durable =True )
	
	n = 0
	while True:
		s = r.group_list()['state']
		n = n + 1

		for x in s:
			arg_body = """Routing Key[%s, %d] ==================================>
XKRX-CS-KR-000252,13:30:48.023942,7,290.9,123.19,90.82,79.62,937.15
XKRX-CS-KR-000253,13:30:48.024171,7,28.84,93.29,67.13,234.64,149.7
XKRX-CS-KR-000257,13:30:48.110733,9,125.17,54.65,374.91,219.27,136.63
""" % (x, n)
			arg_rky = s[x]
			#queueId = channel.queue_declare( exclusive=True, durable =True ).queue
			#channel.queue_bind(queueId, exchange_name, arg_rky)
			print "RabbitMQ Cluster Number", rabbitmq_number, arg_rky, arg_body
			try:

				#self, body, exchange='', routing_key='', mandatory=False, immediate=False, **properties):
				
				channel.basic_publish(arg_body.replace("KR", x), '', arg_rky)
			except Exception, e:
				print "Exception :", e
				exit()
				r = RedisInfo()
				if rabbitmq_number == 0:
					rabbitmq_cluster = 1
				else:
					rabbitmq_cluster = 0
				hostname, port, user, password, vhost, exchange_name, rabbitmq_number = r.rabbitmq(rabbitmq_cluster)
				
				conn = Connection(host=hostname, port=port, userid=user, password=password, virtual_host=vhost)
				channel = conn.channel()
				channel.exchange_declare(exchange_name, type='direct', durable=True)
				channel.basic_publish(arg_body.replace("KR", x), '', arg_rky)
				
					
		time.sleep(1)

	channel.close()
	conn.close()

if __name__ == '__main__':
	Connect()
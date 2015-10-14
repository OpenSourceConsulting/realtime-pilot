# -*- coding: utf-8 -*-
#DataCallBack.py
import datetime
import time

class CallBack:
	def __init__(self):
		self.data_callback_version = 0.1

	def _callback(self):
		############### Biz Logic ################
		n = 0
		while True:
			# redis에 등록된 서비스 group 을 가져옴
			# {'state':{'AA':'XKRX-CS-AA', 'KR':'XKRX-CS-KR'}}, routingkey = 'XKRX-CS-AA', 'XKRX-CS-KR'
			n = n + 1
			x = self.queueId
			t = str( datetime.datetime.now().time() )
			arg_body = """Routing Key[%s, %d] ==================================>\nXKRX-CS-KR-000252,%s,7,290.9,123.19,90.82,79.62,937.15\nXKRX-CS-KR-000253,%s,7,28.84,93.29,67.13,234.64,149.7\nXKRX-CS-KR-000257,%s,9,125.17,54.65,374.91,219.27,136.63""" % (x, n, t, t, t)
			
			############### Biz Logic sesseion #######
			m, r = self._bizlogic( str(arg_body.replace("KR", x)) )

			############### Biz Transmit #############
			self._bizsend(m, r)

			############### Message Delete ###########
			#message.ack()
			time.sleep(1)

	def _bizlogic(self, message_body):
		#message_body
		logic_body = '[' + self.process_idle.name + ', ' + str(self.process_idle.pid) + ', RabbitMQ Cluster : ' + str(self.rabbitmq_cluster) + ', Redis : ' + str(self.redis_server) + ', Time : ' + str( datetime.datetime.now().time() ) + ', Data Callback]\n' + str(message_body)
		return message_body, logic_body

	def _bizsend(self, message_body, redis_body):
		# No exchange_name 
		# Rabbitmq Transmit
		self.rabbitmq_publish(str(message_body), '', self.routingKey)
		
		# Redis Transmit
		self.master_publish('DATA_' + self.routingKey, redis_body)
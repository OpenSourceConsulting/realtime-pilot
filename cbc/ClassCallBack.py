# -*- coding: utf-8 -*-
#ClassCallBack.py
import sys, os
import time
import datetime

class CallBack:
	def __init__(self):
		self.class_callback_version = 0.1

	def _callback(self, message):
		############### Biz Logic ################
		m, r = self._bizlogic( str(message.body) )

		############### Biz Transmit #############
		self._bizsend(m, r)

		############### Message Delete ###########
		message.ack()

	def _bizlogic(self, message_body):
		#message_body
		logic_body = '[' + self.process_idle.name + ', ' + str(self.process_idle.pid) + ', RabbitMQ Cluster : ' + str(self.rabbitmq_cluster) + ', Redis : ' + str(self.redis_server) + ', Time : ' + str( datetime.datetime.now().time() ) + ', Class Callback]\n' + str(message_body)
		return message_body, logic_body

	def _bizsend(self, message_body, redis_body):
		# No exchange_name 
		#self.rabbitmq_publish(str(message_body), '', self.routingKey)
		# Redis Transmit
		self.master_publish(self.queueId, redis_body)

		
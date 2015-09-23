# -*- coding: utf-8 -*-
from librabbitmq import Connection
import sys, os, time
import logging
import numpy as np
import copy
import logging

from netifaces import ifaddresses

sys.path.append(os.environ['QUANT_HOME'] + '/lib')
sys.path.append(os.environ['QUANT_HOME'] + '/cbc')
from Redis import RedisInfo
from CommonClass import Config

################################################################################
# @Author : jebuempak@gmail.com
# @Role   : ServiceClass.py에서 상속되어짐
#           RabbitMQ의 연결 및 상태 정보를 가져옴
# @Traget : Inheritance Class
# @Method : from Rabbitmq import RabbitMQClass
###############################################################################	
class RabbitMQClass( RedisInfo ):
	def __init__(self):
		RedisInfo.__init__(self)
		self.rabbitmq = self.rabbitmq()
		self.new_rabbitmq = copy.deepcopy(self.rabbitmq.keys())
		self.rabbitmq_cluster = 0
		self.hostname = self.rabbitmq[self.rabbitmq_cluster]['hostname']
		self.port = int(self.rabbitmq[self.rabbitmq_cluster]['port'])
		self.user = self.rabbitmq[self.rabbitmq_cluster]['user']
		self.password = self.rabbitmq[self.rabbitmq_cluster]['pass']
		self.vhost = self.rabbitmq[self.rabbitmq_cluster]['vhost']
		self.exchange_name = self.rabbitmq[self.rabbitmq_cluster]['exchange_name']
		#self.queueId = "quantq"
	
	# rabbitmq server cluster number change
	def cluster_random(self):
		self.new_rabbitmq = copy.deepcopy(self.rabbitmq.keys())
		self.new_rabbitmq.remove(self.rabbitmq_cluster)
		self.rabbitmq_cluster = np.random.choice(self.new_rabbitmq, 1)[0]
		self.hostname = self.rabbitmq[self.rabbitmq_cluster]['hostname']
		self.port = int(self.rabbitmq[self.rabbitmq_cluster]['port'])
		self.user = self.rabbitmq[self.rabbitmq_cluster]['user']
		self.password = self.rabbitmq[self.rabbitmq_cluster]['pass']
		self.vhost = self.rabbitmq[self.rabbitmq_cluster]['vhost']
		self.exchange_name = self.rabbitmq[self.rabbitmq_cluster]['exchange_name']

	def rabbitmq_connect(self):
		try:
			self.conn = Connection(host=self.hostname, port=self.port, userid=self.user, password=self.password, virtual_host=self.vhost)
			connect_check = 'True' if self.conn else 'False'
		except Exception, e:
			self.cluster_random()
			self.conn = Connection(host=self.hostname, port=self.port, userid=self.user, password=self.password, virtual_host=self.vhost)
			connect_check = 'True' if self.conn else 'False'

	# rabbitmq cluster server의 상태를 확인 함
	# 
	def rabbitmq_ping(self):
		l = {}
		for x in self.rabbitmq:
			try:
				self.conn = Connection(host=self.rabbitmq[x]['hostname'], port=int(self.rabbitmq[x]['port']), userid=self.rabbitmq[x]['user'], password=self.rabbitmq[x]['pass'], virtual_host=self.rabbitmq[x]['vhost'])
				connect_check = True if self.conn else False
			except:
				connect_check = False
			finally:
				self.conn.close()

			l[x] = {'hostname':self.rabbitmq[x]['hostname'], 'status':connect_check}
		return l
			
		
	def rabbitmq_channel(self):
		self.channel = self.conn.channel()
		self.channel.exchange_declare( self.exchange_name, type='direct', durable=True)
		self.channel.queue_declare( self.queueId, exclusive=False, durable = True)
		##self.channel.queue_bind(self.queueId, self.exchange_name, self.routingKey)

	def rabbitmq_publish(self, message='', exchange_name='',  routingKey='', callback=None):
		properties = {'application_headers': {}, 'delivery_mode': 2, 'content_encoding': u'binary','content_type': u'application/x-python-serialize'}
		try:
			#message = callback
			self.channel.basic_publish(message, exchange_name, routingKey, auto_delete=True)#, **properties)
		except:
			self.rabbitmq_connect()
			self.rabbitmq_channel()
			self.channel.basic_publish(message, exchange_name, routingKey, auto_delete=True)#, **properties)
			
	def rabbitmq_consume(self, callback):
		try:
			self.channel.basic_consume(self.queueId, callback=callback)
			#self.channel.basic_ack(1)
		except KeyboardInterrupt:
			self.channel.close()
			self.conn.close()

		while True:
			try:
				self.conn.drain_events()
			except Exception, e:
				print "rabbitmq_consume : ", e
				self.rabbitmq_connect()
				self.rabbitmq_channel()
				self.rabbitmq_consume(callback)

	def rabbitmq_close(self):
		try:
			pass
		except KeyboardInterrupt:
			self.channel.close()
			self.conn.close()


if __name__ == '__main__':
	r = RabbitMQClass()
	print r.rabbitmq_ping()
	



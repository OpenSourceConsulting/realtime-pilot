# -*- coding: utf-8 -*-
import sys, os, time
import redis
import time

#os.environ['QUANT_HOME'] = '/home/quant'
sys.path.append(os.environ['QUANT_HOME'] + '/lib')
sys.path.append(os.environ['QUANT_HOME'] + '/cbc')

from CommonClass import Config

################################################################################
# @Author : jebuempak@gmail.com
# @Role   : Redis, Memory in DB, RabbitMQ Meta Data, Redis ping, Redis publish
# @Traget : Inheritance Class
# @Method : from Redis import RedisInfo
#           service = RedisInfo().get('service')[myaddress]
###############################################################################	
class RedisInfo:
	def __init__(self):
		cfg = Config()
		
		
		self.rmq = {}
		self.grp = {}

		# Redis master, slave Context
		#self.redis_server = redis.StrictRedis(host=str(self.host), port=int(self.port), db=int(self.dbnm)) #, socket_timeout=-1)
		#self.rdm_slave = redis.StrictRedis(host=str(self.host_slave), port=int(self.port_slave), db=int(self.dbnm_slave) ) #, socket_timeout=1)
	
		#self.redis_server = self.redis_server

		self.redis_list = eval(cfg.get('Redis-List', 'list'))
		self.redis_list_len = len(self.redis_list)

		self.rdm_server = {}
		self.redis_server = None
		self.redis_listup()
		self.redis_current()

	# Redis List Context
	def redis_listup(self):
		for x in range(self.redis_list_len):
			self.rdm_server[x] = redis.StrictRedis( host=self.redis_list[x]['hostname'], port=self.redis_list[x]['port'], db=self.redis_list[x]['db'] )
	
	# Current Live Redis Check
	def redis_current(self):
		for x in self.rdm_server:
			try:
				if self.rdm_server[x].ping(): 
					self.redis_server = self.rdm_server[x]
					break
			except:
				pass
		try:
			return self.redis_server
		except:
			self.redis_listup()
			self.redis_current()
			time.sleep(1)

	# Redis Real Time Check
	def redis_ping(self):
		l = {}
		for x in self.rdm_server:
			try:
				c = self.rdm_server[x].ping()
			except:
				c = False

			l[x] = {'hostname':self.redis_list[x]['hostname'], 'status':c}

		try:
			return l
		except:
			self.redis_listup()
			self.redis_ping()

	# Quant Default Meta Setting
	def set(self):
		#self.rdm = redis.StrictRedis(host=str(self.host), port=int(self.port), db=int(self.dbnm), socket_timeout=1)
		try:
			d = {
				0:{'hostname':'172.31.21.219', 'port':5672, 'user':'quant', 'pass':'quant1234', 'vhost':'dev-quant', 'exchange_name':'quant'},
				1:{'hostname':'172.31.16.52' , 'port':5672, 'user':'quant', 'pass':'quant1234', 'vhost':'dev-quant', 'exchange_name':'quant'}
				}
			self.redis_server.set('rabbitmq', d)

			d = {'state':{'AA':'XKRX-CS-AA', 'KR':'XKRX-CS-KR'}}
			self.redis_server.set('group', d)

			d = {'172.31.7.219':'data', '172.31.7.217':'state', '172.31.7.218':'class', '172.31.7.216':'web'}
			self.redis_server.set('service', d)

		except Exception, e:
			print e
	
	# Quant Meta Get
	def get(self, requestType):
		try:
			self.rst = eval(self.redis_server.get(requestType))
			#print self.rst
		except Exception, e:
			#print 'Get Exception :', e
			self.redis_current()
			#print self.redis_server
			self.rst = eval(self.redis_server.get(requestType))
		return self.rst 
	
	# Redis에 등록된 RabbitMQ Server Address get
	def rabbitmq(self, n = None):
		self.rmq = self.get('rabbitmq')
		#self.rmq = eval(self.redis_server.get('rabbitmq'))
		if type(n) == int:
			return self.rmq[n]['hostname'], int(self.rmq[n]['port']), self.rmq[n]['user'], self.rmq[n]['pass'], self.rmq[n]['vhost'], self.rmq[n]['exchange_name'], int(n)
		else:
			return self.rmq

	def group_list(self):
		self.rmq = self.get('group')
		return self.rmq

	# Redis Publich Function
	def master_publish(self, key, value):
		try:
			self.redis_server.publish(key, value)
		except:
			self.redis_current()
			self.redis_server.publish(key, value)


if __name__ == '__main__':
	r = RedisInfo()
	r.set()
	#print r.get('service')
	#r.rabbitmq
	#
	#while True:
	#	#print r.redis_server
	#	print r.redis_ping()
	#	time.sleep(3)
	
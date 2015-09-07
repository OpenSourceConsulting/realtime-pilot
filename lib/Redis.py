import sys, os
import redis

sys.path.append(os.environ['QUANT_HOME'] + '/lib')
sys.path.append(os.environ['QUANT_HOME'] + '/callback')

import ConfigParser

class RedisInfo:
	def __init__(self):
		cfg = ConfigParser.ConfigParser()
		ini = os.environ['QUANT_HOME'] + '/etc/quant.ini'
		cfg.read(ini)
		#redis master
		self.host = cfg.get('Redis-Master', 'hostname')
		self.port = int(cfg.get('Redis-Master', 'port'))
		self.dbnm = int(cfg.get('Redis-Master', 'db'))

		#redis slave
		self.host_slave = cfg.get('Redis-Slave', 'hostname')
		self.port_slave = int(cfg.get('Redis-Slave', 'port'))
		self.dbnm_slave = int(cfg.get('Redis-Slave', 'db'))

		self.rdm_master = None
		self.rdm_slave = None
		self.rmq = {}
		self.grp = {}
		self.rdm_master = redis.StrictRedis(host=str(self.host), port=int(self.port), db=int(self.dbnm), socket_timeout=1)
		self.rdm_slave = redis.StrictRedis(host=str(self.host_slave), port=int(self.port_slave), db=int(self.dbnm_slave), socket_timeout=1)



	def set(self):
		#self.rdm = redis.StrictRedis(host=str(self.host), port=int(self.port), db=int(self.dbnm), socket_timeout=1)
		try:
			d = {
				0:{'hostname':'172.31.21.219', 'port':5672, 'user':'quant', 'pass':'quant1234', 'vhost':'dev-quant', 'exchange_name':'quant'},
				1:{'hostname':'172.31.16.52' , 'port':5672, 'user':'quant', 'pass':'quant1234', 'vhost':'dev-quant', 'exchange_name':'quant'}
				}
			self.rdm_master.set('rabbitmq', d)
			d = {'state':{'AA':'XKRX-CS-AA', 'KR':'XKRX-CS-KR'}}
			self.rdm_master.set('group', d)
			
		except Exception, e:
			print e
	

	def get(self):
		try:
			self.rmq = eval(self.rdm_slave.get('rabbitmq'))
			self.grp = eval(self.rdm_slave.get('group'))
			print self.rmq
			print self.grp
		except Exception, e:
			print e
	
	def rabbitmq(self, n = None):
		self.rmq = eval(self.rdm_slave.get('rabbitmq'))
		if type(n) == int:
			return self.rmq[n]['hostname'], int(self.rmq[n]['port']), self.rmq[n]['user'], self.rmq[n]['pass'], self.rmq[n]['vhost'], self.rmq[n]['exchange_name'], int(n)
		else:
			return self.rmq

	def rabbitmq_list(self):
		self.rmq = eval(self.rdm_slave.get('rabbitmq'))
		return self.rmq
		#return self.rmq[n]['hostname'], int(self.rmq[n]['port']), self.rmq[n]['user'], self.rmq[n]['pass'], self.rmq[n]['vhost'], self.rmq[n]['exchange_name'], int(n)

	def group_list(self):
		self.grp = eval(self.rdm_slave.get('group'))
		return self.grp

	def class_cluster_set(self, f):
		self.rdm_master.set('cluster', f)


if __name__ == '__main__':
	r = RedisInfo()
	#r.set()
	#r.get()
	print r.rabbitmq()
	
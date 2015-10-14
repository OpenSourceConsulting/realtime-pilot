import sys, os, time
import gevent
import redis
import time

sys.path.append(os.environ['QUANT_HOME'] + '/lib')
sys.path.append(os.environ['QUANT_HOME'] + '/callback')

import ConfigParser
class Test:
	def __init__(self):
		self.master_check = None
		self.slave_check = None
		self.redis_server = None
		gevent.joinall([
		    gevent.spawn(self.mastercheck),
		    gevent.spawn(self.slavecheck),
		    gevent.spawn(self.redis_current)
		    #gevent.spawn(self.loop())  
		])
	

	def mastercheck(self):
		while True:
		    try:
		    	self.master_check = self.rdm_master.ping()
		    except:
		    	self.master_check = False
		    #print('Redis Master : %s' % str(self.master_check))
		    gevent.sleep(0.3)

	def slavecheck(self):
		while True:
		    try:
		    	self.slave_check = self.rdm_slave.ping()
		    except:
		    	self.slave_check = False
		    #print('Redis Slave : %s' % str(self.slave_check))
		    gevent.sleep(0.3)

	def redis_current(self):
		"""
		try: 
			self.master_check = self.rdm_master.ping()
		except Exception, e:
			print 'Master :', e
			self.master_check = False

		try: 
			self.slave_check = self.rdm_slave.ping()
		except Exception, e:
			print 'Slave :', e
			self.slave_check = False
		"""
		while True:
			if self.master_check == True:
				self.redis_server = self.rdm_master
			elif self.slave_check == True:
				self.redis_server = self.rdm_slave
			gevent.sleep(1)

	
class RedisInfo:
	def __init__(self):
		#Test.__init__(self)
		cfg = ConfigParser.ConfigParser()
		ini = os.environ['QUANT_HOME'] + '/etc/quant.ini'
		cfg.read(ini)

		self.rmq = {}
		self.grp = {}

		self.rdm_server = {}
		self.redis_listup()

	def redis_listup(self):
		for x in range(self.redis_list_len):
			self.rdm_server[x] = redis.StrictRedis( host=self.redis_list[x]['hostname'], port=self.redis_list[x]['port'], db=self.redis_list[x]['db'] )
		
	def redis_current(self):
		for x in self.rdm_server:
			try:
				if self.rdm_server[x].ping(): self.redis_server = self.rdm_server[x]
				break
			except:
				pass
		try:
			return self.redis_server
		except:
			self.redis_listup()
			self.redis_current()
			time.sleep(1)

	def get(self, requestType):
		while True:
			try:
				self.rst = eval(self.redis_server.get(requestType))
			except:
				self.redis_current()
				self.rst = eval(self.redis_server.get(requestType))

			print self.redis_server
			print self.rst
			print ''

			gevent.sleep(1)
			#return self.rst 


if __name__ == '__main__':
	r = RedisInfo()
	print r.get('group')


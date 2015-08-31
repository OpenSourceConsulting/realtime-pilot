import sys, os
import redis

sys.path.append(os.environ['QUANT_HOME'] + '/lib')
sys.path.append(os.environ['QUANT_HOME'] + '/callback')

import ConfigParser

class RedisInfo():
	def __init__(self, cmd='get'):
		cfg = ConfigParser.ConfigParser()
		ini = os.environ['QUANT_HOME'] + '/etc/quant.ini'
		cfg.read(ini)
		self.host = cfg.get('Redis', 'hostname')
		self.port = int(cfg.get('Redis', 'port'))
		self.dbnm = int(cfg.get('Redis', 'db'))
		self.rdm = None
		self.rmq = {}
		self.grp = {}

		self.rdm = redis.StrictRedis(host=str(self.host), port=int(self.port), db=int(self.dbnm), socket_timeout=1)

		"""
		try:
			d = {'hostname':'172.31.21.219', 'port':5672, 'user':'quant', 'pass':'quant1234'}
			self.rdm.set('rabbitmq', d)
			self.rmq = eval(self.rdm.get('rabbitmq'))
			
		except Exception, e:
			print e
		"""

		if cmd == 'get':
			self.get()
		elif cmd == 'set':
			self.set()

	def set(self):
		#self.rdm = redis.StrictRedis(host=str(self.host), port=int(self.port), db=int(self.dbnm), socket_timeout=1)
		try:
			d = {'hostname':'172.31.21.219', 'port':5672, 'user':'quant', 'pass':'quant1234', 'vhost':'dev-quant'}
			self.rdm.set('rabbitmq', d)
			#self.rmq = eval(self.rdm.get('rabbitmq'))
			d = {'state':{'AA':'XKRX-CS-AA', 'KR':'XKRX-CS-KR'}}
			self.rdm.set('group', d)
			
		except Exception, e:
			print e
		#for x in l:
		#	print x

	def get(self):
		#self.rdm = redis.StrictRedis(host=str(self.host), port=int(self.port), db=int(self.dbnm), socket_timeout=1)
		try:
			#d = {'hostname':'172.31.21.219', 'port':5672, 'user':'admin', 'pass':'opensource'}
			self.rmq = eval(self.rdm.get('rabbitmq'))
			self.grp = eval(self.rdm.get('group'))
			
		except Exception, e:
			print e
		#for x in l:
		#	print x

if __name__ == '__main__':
	r = RedisInfo(sys.argv[1])
	#r.run()
	"""
	print r.rmq['hostname']
	print r.rmq['port']
	print r.rmq['user']
	print r.rmq['pass']
	print r.rmq['vhost']
	"""
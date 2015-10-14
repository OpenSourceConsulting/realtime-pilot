import sys, os
import redis
from redis.sentinel import Sentinel, SentinelConnectionPool,ConnectionError, MasterNotFoundError, SlaveNotFoundError
import time

sys.path.append(os.environ['QUANT_HOME'] + '/lib')
sys.path.append(os.environ['QUANT_HOME'] + '/callback')

import ConfigParser
from Redis import RedisInfo 
cfg = ConfigParser.ConfigParser()
ini = os.environ['QUANT_HOME'] + '/etc/quant.ini'
cfg.read(ini)

r = RedisInfo()

n = 0
while True:
    r.master_publish('test', 'this will reach the listener %d' % n)
    time.sleep(1)
    n = n + 1
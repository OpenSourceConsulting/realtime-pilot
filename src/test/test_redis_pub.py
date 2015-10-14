# -*- coding: utf-8 -*-
import zmq
import time
import sys, os
import random

# python /home/ec2-user/source/Web/websocket/examples/WebSocket_pub.py 10004 DATA_XKRX-CS-KR &
# python /home/ec2-user/source/Web/websocket/examples/WebSocket_pub.py 10002 XKRX-CS-KR &
# python /home/ec2-user/source/Web/websocket/examples/WebSocket_pub.py 10003 KR &

sys.path.append(os.environ['QUANT_HOME'] + '/lib')
#from Redis import RedisInfo

#r = RedisInfo()

from redis import Redis, exceptions, RedisError
from redis.sentinel import (Sentinel, SentinelConnectionPool,ConnectionError, MasterNotFoundError, SlaveNotFoundError)

# Redis 접속 기본 설정값
listSentinel = [('172.31.5.41', 26379)]
strServiceName = 'mymaster'
strRedisPass = ''
nDB = 0

sentinel = Sentinel(listSentinel, socket_timeout=0.1)
master = sentinel.master_for(strServiceName, password=strRedisPass, db=nDB, socket_timeout=0.1)
slave = sentinel.slave_for(strServiceName, password=strRedisPass, db=nDB, socket_timeout=0.1)
    

rds = master

print master
n = 'Text'
while True:
	r = random.randrange(0,2)
	key = str( r ) + "_" + n + "_" + str( r )
	value = key + " " + n*(random.randrange(0,10))
	print key, value
	rds.publish(key, value)
	time.sleep(1)

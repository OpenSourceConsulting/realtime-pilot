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

sentinel = Sentinel(listSentinel, socket_timeout=1)
master = sentinel.master_for(strServiceName, password=strRedisPass, db=nDB, socket_timeout=1)
slave = sentinel.slave_for(strServiceName, password=strRedisPass, db=nDB, socket_timeout=1)
    

rds = master
rds_pub = rds.pubsub()
rds_pub.subscribe('0_Text_0')

"""
print sys.argv[1]
"""
while True:
        try:
                for x in rds_pub.listen():
                        print "Text :", str(x['data'])
        except Exception e:
                print e
                pass



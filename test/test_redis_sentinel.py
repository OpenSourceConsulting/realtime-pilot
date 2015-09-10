# -*- coding:utf-8 -*-

import sys, random, time
from redis import Redis, exceptions, RedisError
from redis.sentinel import (Sentinel, SentinelConnectionPool,ConnectionError,
                            MasterNotFoundError, SlaveNotFoundError)

# Redis 접속 기본 설정값
listSentinel = [('172.31.5.41', 26379)]
strServiceName = 'mymaster'
strRedisPass = ''
nDB = 0

nMaxUser = 1000

sentinel = Sentinel(listSentinel, socket_timeout=0.1)
try:
    #sentinel.discover_master(strServiceName) # No need for this
    #sentinel.discover_slaves(strServiceName)
    master = sentinel.master_for(strServiceName, password=strRedisPass, db=nDB, socket_timeout=0.1)
    slave = sentinel.slave_for(strServiceName, password=strRedisPass, db=nDB, socket_timeout=0.1)
    for x in dir(master):
        print x
    print dir(master.info)
    exit()
except MasterNotFoundError:
    print 'Master not found or Sentinel instances not runnung'
    sys.exit()
except SlaveNotFoundError:
    print 'Slave not found or Sentinel instances not runnung'
    sys.exit()
except ConnectionError:
    print 'Connection Error. Check if Sentinel instances are running'
    sys.exit()

start_time = time.time()

for n in range(1, nMaxUser):
    for m in range(1, random.randint(0, 5)):
        master.hset( "cart.user:"+str(n), random.randint(1, 300), random.randint(1, 5) )

time_elapsed_1 = time.time() - start_time

start_time = time.time()

for n in range(1, nMaxUser):
    slave.hgetall("cart.user:"+str(n))

time_elapsed_2 = time.time() - start_time

count = 0

for n in range(1, nMaxUser):
    data = slave.hgetall("cart.user:"+str(n))
    if len(data) > 0:
        count = count + 1
        print count, " [Cart.user:"+str(n)+"] ", data

print "---------------------------------------------------"
print "[Time for writing]: ", time_elapsed_1, " sec., [Time for reading]: ", time_elapsed_2, " sec."

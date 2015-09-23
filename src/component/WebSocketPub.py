import zmq
import time
import sys, os

# python /home/ec2-user/source/Web/websocket/examples/WebSocket_pub.py 10004 DATA_XKRX-CS-KR &
# python /home/ec2-user/source/Web/websocket/examples/WebSocket_pub.py 10002 XKRX-CS-KR &
# python /home/ec2-user/source/Web/websocket/examples/WebSocket_pub.py 10003 KR &

sys.path.append(os.environ['QUANT_HOME'] + '/lib')
from Redis import RedisInfo

r = RedisInfo()
rds = r.redis_server
rds_pub = rds.pubsub()
rds_pub.subscribe([sys.argv[2]])

c = zmq.Context()
s = c.socket(zmq.PUB)
s.bind('tcp://127.0.0.1:%s' % (sys.argv[1]) )
while(True):
        try:
                for x in rds_pub.listen():
                        s.send( str(x['data']) )
        except Exception, e:
                #print e
                r.redis_current()
                rds = r.redis_server
                rds_pub = rds.pubsub()
                rds_pub.subscribe([sys.argv[2]])
                #for x in rds_pub.listen():
                #       s.send( str(x['data']) )

        #time.sleep(1)

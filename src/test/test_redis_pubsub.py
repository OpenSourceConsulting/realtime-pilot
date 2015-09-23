import sys, os
import redis
from redis.sentinel import Sentinel, SentinelConnectionPool,ConnectionError, MasterNotFoundError, SlaveNotFoundError
import time
import threading

sys.path.append(os.environ['QUANT_HOME'] + '/lib')
sys.path.append(os.environ['QUANT_HOME'] + '/callback')
from Redis import RedisInfo

redis_r = RedisInfo().master
class Listener(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)
    
    def work(self, item):
        print item['channel'], ":", item['data']
    
    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == "KILL":
                self.pubsub.unsubscribe()
                print self, "unsubscribed and finished"
                break
            else:
                self.work(item)

if __name__ == "__main__":
    r = redis_r #redis.Redis(host=host, port=port, db=db)
    a = r.pubsub()
    b = a.subscribe(['KR'])
    for x in a.listen():
        print x['data']
        #a.unsubscribe()

    #client = Listener(r, ['KR'])
    #client.start()
    
    """
    r.publish('test', 'this will reach the listener')
    r.publish('fail', 'this will not')
    
    r.publish('test', 'KILL')
    """
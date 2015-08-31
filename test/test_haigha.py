import sys
from haigha.connection import Connection
from haigha.message import Message

sys.path.append("/home/ec2-user/source/Quant/component")

import rdm
r = rdm.RedisInfo()

connection = Connection(
  host=r.rmq['hostname'], port=r.rmq['port'],
  user=r.rmq['user'], password=r.rmq['pass'],
  vhost='/', heartbeat=None, debug=True)

ch = connection.channel()
ch.exchange.declare('test_exchange', 'direct')
ch.queue.declare('test_queue', auto_delete=True)
ch.queue.bind('test_queue', 'test_exchange', 'test_key')
ch.basic.publish( Message('body', application_headers={'hello':'world'}), exchange='test_exchange', routing_key='test_key' )
mq = ch.basic.get('test_queue')
connection.close()

print mq
#!/usr/bin/env python

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
import datetime
import sys
from optparse import OptionParser as parser

sys.path.append("/home/ec2-user/source/Quant/component")
import rdm #rabbitmq address info

r = rdm.RedisInfo()
hostname = r.rmq['hostname']
port = r.rmq['port']
user = r.rmq['user']
password = r.rmq['pass']
vhost = r.rmq['vhost']
exchange_name = 'q3'

class Service( object ):

    def __init__( self, groups, host = 'localhost', verbose = True, port = 5672, user = '', password = '' ):
        credentials = PlainCredentials(user, password)
        self._connection = BlockingConnection( ConnectionParameters( host,  port, vhost, credentials ) )
        self._channel = self._connection.channel()
        self._channel.exchange_declare( exchange = exchange_name, type = 'topic' )
        self._queueID = self._channel.queue_declare( exclusive = True ).method.queue

        for topic in groups:
            self._channel.queue_bind(exchange = exchange_name, queue = self._queueID, routing_key = topic)
            
    def _handle( self, c, m, p, b):
        print b
        

    def close( self ):

        self._channel.stop_consuming()
        print 'done', datetime.datetime.now()

        self._connection.close()

    def run( self ):
        self._channel.basic_consume( self._handle, queue = self._queueID, no_ack = True )
        self._channel.start_consuming()

def main():

    f = parser()
    f.add_option( '-g', '--groups', help = 'group specifiers', dest = 'groups', default = '#' )

    options, args = f.parse_args()

    groups = options.groups.split( ',' )
    #topics = [ 'SS.' + g for g in groups ]
    #print topics

    s = Service( groups, host=hostname, port=port, user=user, password=password )
    try:
        s.run()
    except KeyboardInterrupt:
        s.close()

if __name__ == '__main__':

    sys.exit( main() )

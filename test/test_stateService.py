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

    def __init__( self, topics, name, host = 'localhost', verbose = True, port = 5672, user = '', password = ''  ):
        credentials = PlainCredentials(user, password)
        self.connection = BlockingConnection( ConnectionParameters( host,  port, vhost, credentials ) )
        self.channel = self.connection.channel()
        self.channel.exchange_declare( exchange = exchange_name, type = 'topic' )
        self.queueID = self.channel.queue_declare( exclusive = True ).method.queue
        self.name = name

        for topic in topics:
            self.channel.queue_bind( exchange = exchange_name, queue = self.queueID, routing_key = topic)

    def _handle( self, c, m, p, b ):
        routingKey = self.name #'.'.join( [ 'SS', self.name ] )
        print routingKey, b
        self.channel.basic_publish( exchange = exchange_name, routing_key = routingKey, body = b)

    def close( self ):

        self.channel.stop_consuming()
        print 'done', datetime.datetime.now()
        #for key, val in self._deposit.iteritems():
        #    print key, len( val )

        self.connection.close()

    def run( self ):

        #_callback = lambda c, m, p, d: self._handle( d )
        self.channel.basic_consume( self._handle, queue = self.queueID, no_ack = True )
        self.channel.start_consuming()

            
def main():

    f = parser()
    f.add_option( '-g', '--groups', help = 'group specifiers', dest = 'groups', default = '#' )
    f.add_option( '-n', '--name', help = 'name', dest = 'name' )

    options, args = f.parse_args()

    groups = options.groups.split( ',' )
    #topics = [ 'DS.' + g for g in groups ]
    topics = groups

    print topics

    s = Service( topics, options.name, host=hostname, port=port, user=user, password=password )
    try:
        s.run()
    except KeyboardInterrupt:
        s.close()

if __name__ == '__main__':

    sys.exit( main() )

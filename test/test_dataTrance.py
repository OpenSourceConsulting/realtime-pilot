#!/usr/bin/env python

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
#from  SelectConnection
import datetime 
import time, random, math
import sys
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
    def __init__( self, host = 'localhost', port = 5672, user = '', password = '', vhost = '/', routingKey = ''):
        credentials = PlainCredentials( user, password )
        self._connection = BlockingConnection( ConnectionParameters( host,  port, vhost, credentials ) )
        #self._connection = SelectConnection( ConnectionParameters( host,  port, vhost, credentials ) )
        self._channel = self._connection.channel()
        self._channel.exchange_declare( exchange = exchange_name, type = 'topic' )
        self.rkey = routingKey
        
    def close( self ):
        self._connection.close()

    def run( self ):
        #message = raw_input("Message : ")
        while True:
            message = """
            XKRX-CS-KR-000252,13:30:48.023942,7,290.9,123.19,90.82,79.62,937.15
            XKRX-CS-KR-000253,13:30:48.024171,7,28.84,93.29,67.13,234.64,149.7
            XKRX-CS-KR-000254,13:30:48.024337,7,248.17,118.49,1489.54,118.45,117.42
            XKRX-CS-KR-000255,13:30:48.024497,7,70.67,170.82,65.45,152.11,420.7
            XKRX-CS-KR-000256,13:30:48.034801,7,160.74,82.36,260.87,104.42,384.35
            XKRX-CS-KR-000257,13:30:48.034973,7,123.39,150.31,60.78,201.21,181.55
            XKRX-CS-KR-000100,13:30:48.035137,8,166.66,87.45,252.83,82.03,44.02
            XKRX-CS-KR-000101,13:30:48.045434,8,114.86,1023.0,37.92,65.76,61.82
            XKRX-CS-KR-000102,13:30:48.045586,8,159.16,97.96,60.07,75.29,690.15
            XKRX-CS-KR-000103,13:30:48.045730,8,23.52,133.91,44.0,107.83,533.96
            XKRX-CS-KR-000104,13:30:48.045901,8,76.62,274.25,166.57,116.48,149.1
            XKRX-CS-KR-000250,13:30:48.056203,8,105.32,254.87,158.97,21.0,59.72
            XKRX-CS-KR-000251,13:30:48.056364,8,192.7,226.26,76.02,72.7,40.53
            XKRX-CS-KR-000252,13:30:48.056520,8,138.58,138.76,89.68,41.78,175.83
            XKRX-CS-KR-000253,13:30:48.066883,8,88.67,41.84,126.81,222.26,8.98
            XKRX-CS-KR-000254,13:30:48.067103,8,156.14,126.11,46.24,24.03,57.94
            XKRX-CS-KR-000255,13:30:48.067259,8,136.01,35.25,25.29,275.88,50.33
            XKRX-CS-KR-000256,13:30:48.067416,8,136.89,10.51,197.03,200.62,238.65
            XKRX-CS-KR-000257,13:30:48.077776,8,47.36,41.77,101.75,105.99,64.56
            XKRX-CS-KR-000100,13:30:48.078006,9,26.76,231.9,104.19,117.87,24.69
            XKRX-CS-KR-000101,13:30:48.078187,9,57.14,84.92,73.62,33.72,47.86
            XKRX-CS-KR-000102,13:30:48.088561,9,21.85,120.6,538.69,58.24,1685.93
            XKRX-CS-KR-000103,13:30:48.088819,9,450.32,417.01,210.68,121.41,27.18
            XKRX-CS-KR-000104,13:30:48.088998,9,80.61,69.15,132.51,98.67,226.2
            XKRX-CS-KR-000250,13:30:48.089161,9,107.44,11.22,80.1,85.93,125.1
            XKRX-CS-KR-000251,13:30:48.099518,9,43.86,51.79,282.43,101.35,946.29
            XKRX-CS-KR-000252,13:30:48.099705,9,170.75,242.6,74.15,323.43,28.48
            XKRX-CS-KR-000253,13:30:48.099871,9,53.27,36.47,81.75,50.96,46.73
            XKRX-CS-KR-000254,13:30:48.110195,9,136.93,17.66,77.64,253.57,66.8
            XKRX-CS-KR-000255,13:30:48.110408,9,65.49,72.59,39.59,63.07,74.31
            XKRX-CS-KR-000256,13:30:48.110575,9,63.16,44.29,36.04,119.36,21.78
            XKRX-CS-KR-000257,13:30:48.110733,9,125.17,54.65,374.91,219.27,136.63
            """
            self._channel.basic_publish( exchange = exchange_name, routing_key = self.rkey, body = message )
            print 'Done', datetime.datetime.now(), ", Message :", message
        self.close()



def main():
    s = Service( host=hostname, port=port, user=user, password=password, vhost=vhost, routingKey=sys.argv[1] )
    s.run()
    #s.close()

if __name__ == '__main__':

    sys.exit( main() )

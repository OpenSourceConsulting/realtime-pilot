from librabbitmq import Connection
import time
import sys
sys.path.append("/home/ec2-user/source/Quant/component")

import rdm

r = rdm.RedisInfo()
hostname = r.rmq['hostname']
port = r.rmq['port']
user = r.rmq['user']
password = r.rmq['pass']
vhost = r.rmq['vhost']
exchange_name = 'quant'

#arg_exchange    = sys.argv[1]
#arg_que       = sys.argv[1]
#arg_rky       = sys.argv[1]
#arg_body      = sys.argv[3]


def Connect():
	conn = Connection(host=hostname, port=port, userid=user, password=password, virtual_host=vhost)
	channel = conn.channel()
	channel.exchange_declare(exchange_name, 'topic')

	while True:
		s = r.grp['state']

		for x in s:
			arg_body = """Routing Key[%s] ==================================>
XKRX-CS-KR-000252,13:30:48.023942,7,290.9,123.19,90.82,79.62,937.15
XKRX-CS-KR-000253,13:30:48.024171,7,28.84,93.29,67.13,234.64,149.7
""" % x
			arg_rky = s[x]
			print arg_rky, arg_body
			channel.basic_publish(arg_body.replace("KR", x), exchange_name, arg_rky)
		
		time.sleep(5)

	channel.close()
	conn.close()

if __name__ == '__main__':
	Connect()
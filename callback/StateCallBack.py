#StateCallBack.py
import sys, os, time

class CallBack:
	def __init__(self):
		self.state_callback_version = 0.1

	def _callback(self, m):
		msg_body = m.body
		rstBody = '[' + self.process_idle.name + ', ' + str(self.process_idle.pid) + '],  State Callback === ' + str(msg_body) + '\n\n'

		print "RabbitMQ Cluster Number %s %s" % (str(self.rabbitmq_cluster), self.routingKey)
		print m.properties, dir(m)
		print rstBody
		try:
			self.channel.basic_publish(rstBody, '', self.routingKey)
			#self.channel.basic_ack(0)
		except Exception, e:
			print "State Exception :", e
		

#StateCallBack.py
import sys, os

class CallBack:
	def __init__(self):
		self.version = 0.1

	def _callback(self, m):
		rstBody = '[' + self.process_idle.name + ', ' + str(self.process_idle.pid) + '],  State Callback === ' + str(m.body) + '\n\n'
		print rstBody
		self.channel.basic_publish(rstBody, self.exchange_name, self.csGroup)


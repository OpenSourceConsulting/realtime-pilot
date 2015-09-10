#DataCallBack.py
import sys, os

class CallBack:
	def __init__(self):
		self.version = 0.1

	def _callback(self):
		rstBody = '[' + self.process_idle.name + ', ' + str(self.process_idle.pid) + '], Class Callback === ' + str(m.body) + '\n\n'
		print rstBody
		return None
		#self.channel.basic_publish(arg_body.replace("KR", x), exchange_name, arg_rky)
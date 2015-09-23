# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.environ['QUANT_HOME'] + '/lib')
sys.path.append(os.environ['QUANT_HOME'] + '/cbc')

import ConfigParser

################################################################################
# @Author : jebuempak@gmail.com
# @Role   : /home/quant/etc/quant.ini file에 구성된 Config 값들을 자져옴
# @Traget : CommonClass
# @Mehtod : cfg = Config(), cfg.get(section, option)
###############################################################################	
class Config:
	def __init__(self):
		self.cfg = ConfigParser.ConfigParser()
		ini = os.environ['QUANT_HOME'] + '/etc/quant.ini'
		self.cfg.read(ini)

	def get(self, section, option):
		return self.cfg.get(section, option)
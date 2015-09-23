# -*- coding: utf-8 -*-
##########
## 테스트 
##########
import sys, os
sys.path.append(os.environ['QUANT_HOME'] + '/lib')

from CommonClass import Config

from netifaces import ifaddresses


cfg = Config()
print cfg.get('Manager', 'pid_file')
print cfg.get('Manager', 'manager_host')
print ""
print eval(cfg.get('Server', 'ipaddress'))
#print sys.path


#print ("%s/bin/QuantService &") % (os.environ['QUANT_HOME'])
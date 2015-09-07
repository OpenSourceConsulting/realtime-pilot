import psutil
import time
import os

"""
parent = psutil.Process(parent_pid)
for child in parent.children(recursive=True):  # or parent.children() for recursive=False
    child.kill()
parent.kill()
"""

def kill(parent_pid):
	parent = psutil.Process(parent_pid)
	for child in parent.children(recursive=True):  # or parent.children() for recursive=False
		child.kill()
	parent.kill()

def checked(n):
	check = 0
	for x in psutil.pids():
		p = psutil.Process(x)
		
		if os.path.basename(n) in p.cmdline():
			check = 1
			break

	return check

def listup(n):
	check = 1
	for x in psutil.pids():
		p = psutil.Process(x)
		#print p.cmdline()

		if n != p.cmdline():
			check = 0
		
		if n == p.cmdline(): #p.name():
			print p.name(), p.ppid(), p.pid, p.cmdline()
			#kill(p.ppid())
			#p.kill()
			check = 1
			break

	return check
		

while True:
	check = checked('/home/ec2-user/source/Quant/test/test_multiprocess.py')
	if check == 0:	
		command = ['/usr/bin/python', 'python', '/home/ec2-user/source/Quant/test/test_multiprocess.py']
		os.spawnlp(os.P_NOWAIT, *command)
	
	time.sleep(1)



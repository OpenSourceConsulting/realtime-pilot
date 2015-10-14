import sys, os
import time
import zipfile


sys.path.append(os.environ['QUANT_HOME'] + '/lib')
from Redis import RedisInfo

redis = RedisInfo().rdm_master

directory = '/home/ec2-user/source/Quant/resource/cluster'
redis_file= '/home/ec2-user/source/Quant/resource/redis_file'


def file_open(f):
	return open(f, "rb").read()

def file_write(f, data):
	return open(f, 'wb').write(data)

# This would print all the files and directories
dirs = os.listdir( directory )
for file in dirs:
   file_name = os.path.basename(file)
   print "Redis Upload :", file,
   redis.set(file_name, file_open( directory + '/' + file))
   print "Complete!"

for file in dirs:
	print "Redis Write :", file,
	#file_write( redis_file + '/' + file, redis.get(file_name) )
	zf = zipfile.ZipFile(redis.get(file_name), 'r')
	print zf.namelist()

	print "Complete!"

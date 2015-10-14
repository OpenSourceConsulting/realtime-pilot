yum install zeromq -y
#curl -O http://python-distribute.org/distribute_setup.py
curl -O https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
python get-pip.py
pip install pyzmq 14.7.0
pip install paste
pip install gevent
pip install gevent_zeromq
pip install librabbitmq
pip install netifaces
pip install cython
pip install redis


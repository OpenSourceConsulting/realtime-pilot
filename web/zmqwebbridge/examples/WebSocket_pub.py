import zmq
import time

c = zmq.Context()
s = c.socket(zmq.PUB)
s.bind('tcp://127.0.0.1:10003')
while(True):
    for c  in  range(100):
        print 'Test :', c
        s.send('Test :' + str(c))
        time.sleep(1)
# -*- coding: utf-8 -*-
import sys
import zmq
import time

REQUEST_TIMEOUT = 1000*60*60*24*365 #365 Day
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://172.31.7.216:5871"

context = zmq.Context()

print "I: Connecting to server…"
client = context.socket(zmq.REQ)
client.connect(SERVER_ENDPOINT)

poll = zmq.Poller()
poll.register(client, zmq.POLLIN)

sequence = 0
retries_left = REQUEST_RETRIES
while True: #retries_left:
    sequence += 1
    request = str(sequence) + "test"
    print "1 I: Sending (%s)" % request

    try:
        print "try",
        client.send(request)
        socks = dict(poll.poll(REQUEST_TIMEOUT))
        print socks
        
        if socks.get(client) == zmq.POLLIN:
            reply = client.recv()
            if not reply:
                break
            print "Replay 1 :", reply
    except Exception, e:
        print "except", e
        client.setsockopt(zmq.LINGER, 0)
        client.close()
        poll.unregister(client)
        
        # Create new connection
        client = context.socket(zmq.REQ)
        client.connect(SERVER_ENDPOINT)
        poll.register(client, zmq.POLLIN)
        client.send(request)
        if socks.get(client) == zmq.POLLIN:
            reply = client.recv()
            if not reply:
                break
            print "Replay 2 :", reply

    time.sleep(1)
    """
    expect_reply = True
    while expect_reply:
        socks = dict(poll.poll(REQUEST_TIMEOUT))
        print "11 ", socks.get(client)
        print "22 ", zmq.POLLIN
        if socks.get(client) == zmq.POLLIN:
            reply = client.recv()
            if not reply:
                break
            print "Replay :", reply
            
            if int(reply) == sequence:
                print "2 I: Server replied OK (%s)" % reply
                retries_left = REQUEST_RETRIES
                expect_reply = False
            else:
                print "3 E: Malformed reply from server: %s" % reply
        else:
            print "4 W: No response from server, retrying…"
            # Socket is confused. Close and remove it.
            client.setsockopt(zmq.LINGER, 0)
            client.close()
            poll.unregister(client)
            retries_left -= 1
            if retries_left == 0:
                print "5 E: Server seems to be offline, abandoning"
                break
            print "6 I: Reconnecting and resending (%s)" % request
            # Create new connection
            client = context.socket(zmq.REQ)
            client.connect(SERVER_ENDPOINT)
            poll.register(client, zmq.POLLIN)
            client.send(request)
    """

context.term()
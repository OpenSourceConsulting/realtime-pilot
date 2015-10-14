# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import gevent
import time, sys, os
from threading import Thread
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, close_room, disconnect

#########################
# Quant Redis Configure #
#########################
sys.path.append(os.environ['QUANT_HOME'] + '/lib')
from Redis import RedisInfo
r = RedisInfo()
rds = r.redis_server
import Daemon
from CommonClass import Config
# quant config text file read
cfg = Config()
port = int(cfg.get('WebServer', 'port'))
##########################

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(10)
        count += 1
        socketio.emit('my response', {'data': 'Server generated event' + '\n', 'count': count}, namespace='/quant')

@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('flask.html')


@socketio.on('my event', namespace='/quant')
def message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'] + '\n', 'count': session['receive_count']})

##############################################################################
# @Author : jebuempak@gmail.com
# @Role   : WebSocket Server
# @Traget : 사용자가 선택한 Topic을 화면에 전달함
# @Method : /home/quant/bin/WebSocketServer or python /home/quant/src/component/WebSocketServer.py
# @Used   : Yes
###############################################################################         
@socketio.on('service state', namespace='/quant')
def service_data(message):
    global r #redis class
    global rds #redis context
    q = r.get('group')['state'] #quant service dict

    #print dir(request.namespace)
    #print request.namespace.ns_name

    def process():
        rds_pub = rds.pubsub()
        rds_pub.subscribe(['service_state'])
        for x in rds_pub.listen():
            socketio.emit('service_state', {'data': str(x['data']) + '\n'}, namespace='/quant') 
        gevent.sleep(1)

    def listen(res, qkey, rkey):
        while True:
            try:
                rds_pub = rds.pubsub()
                if res == 'data': rds_pub.subscribe([ 'DATA_' + rkey ])
                if res == 'state':rds_pub.subscribe([ rkey ])
                if res == 'class':rds_pub.subscribe([ qkey ])
                for x in rds_pub.listen():
                    socketio.emit(res + '_response', {'qkey':qkey, 'data': str(x['data']) + '\n'}, namespace='/quant') #broadcast=True)
            except Exception, e:
                    r.redis_current()
                    rds = r.redis_server
                    rds_pub = rds.pubsub()
            gevent.sleep(0.3)

    ################## coroutin thred start #############################
    gevent_threds = []
    for x in ['data', 'state', 'class']:
        for y in q:
            gevent_threds.append( gevent.spawn(listen, x, y, q[y]) )
    gevent_threds.append( gevent.spawn(process) )
    gevent.joinall( gevent_threds )
    ################## coroutin thred end ###############################
    
""""
@socketio.on('disconnect request', namespace='/quant')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('disconnect', namespace='/quant')
def test_disconnect():
    print 'Connect'
    print('Client disconnected')
"""
@socketio.on('connect', namespace='/quant')
def connect():
    emit('my response', {'data': 'Connected' + '\n', 'count': 0})

if __name__ == '__main__':
    Daemon.Daemon(pidfile='/tmp/webserver.pid').runAsDaemon()
    socketio.run(app, host='0.0.0.0', port=port)

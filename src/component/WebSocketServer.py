# -*- coding: utf-8 -*-
import gevent
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import logging
import sys, os
sys.path.append(os.environ['QUANT_HOME'] + '/lib')
import wsbridge
import json
import daemon

logging.basicConfig(level=logging.DEBUG)

class MyBridgeClass(wsbridge.BridgeWebProxyHandler):
    def zmq_allowed(self, params):
        params = json.loads(params)
        #print params
        zmq_conn_string = params['zmq_conn_string']
        socket_type = params['socket_type']
        #print 'auth', params['username'], params['socket_type']
        return params['username'] == 'hugo'
        

class MyWsgiHandler(wsbridge.WsgiHandler):
    bridge_class = MyBridgeClass
    def websocket_allowed(self, environ):
        #you can add logic here to do auth
        return True


def main(host='127.0.0.1', port=8001):
  app = MyWsgiHandler()
  server = pywsgi.WSGIServer((host, port), app.wsgi_handle,
                           # keyfile='/etc/nginx/server.key',
                           # certfile='/etc/nginx/server.crt',
                           handler_class=WebSocketHandler)
  server.serve_forever()

if __name__ == '__main__':
  #with daemon.DaemonContext():
  main()
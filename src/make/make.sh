cython --embed -o QuantService.c /home/quant/src/component/QuantService.py
gcc -Os -I /usr/include/python2.7 -o QuantService QuantService.c -lpython2.7 -lpthread -lm -lutil -ldl

cython --embed -o QuantManager.c /home/quant/src/component/QuantManager.py
gcc -Os -I /usr/include/python2.7 -o QuantManager QuantManager.c -lpython2.7 -lpthread -lm -lutil -ldl

cython --embed -o WebSocketServer.c /home/quant/src/component/WebSocketServer.py
gcc -Os -I /usr/include/python2.7 -o WebSocketServer WebSocketServer.c -lpython2.7 -lpthread -lm -lutil -ldl

cp -rf QuantManager QuantService WebSocketServer /home/quant/bin

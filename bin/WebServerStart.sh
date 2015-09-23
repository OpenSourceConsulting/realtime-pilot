/home/quant/bin/QuantManager server
/home/quant/bin/WebSocketServer &

#python //home/ec2-user/source/Quant/comment/Middleware.py &
/home/quant/bin/WebSocketPub 10004 DATA_XKRX-CS-KR &
/home/quant/bin/WebSocketPub 10002 XKRX-CS-KR &
/home/quant/bin/WebSocketPub 10003 KR &

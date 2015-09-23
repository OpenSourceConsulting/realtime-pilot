ps -ef | grep Quant | grep "Quant" | awk {'print "kill -9 " $2'} | sh -x
ps -ef | grep WebSocket | grep "WebSocket" | awk {'print "kill -9 " $2'} | sh -x

ps -ef | grep Quant | grep "Quant" | awk {'print "kill -9 " $2'} | sh -x

context = new zmq.Context('ws://52.68.73.241:8000');


reqrep = context.Socket(zmq.REQ);
reqrep.connect('tcp://127.0.0.1:10001', {'username':'hugo'});

/*
reqrep2 = context.Socket(zmq.REQ);
reqrep2.connect('tcp://127.0.0.1:10001', {'username':'hugo'});
reqrep.send('hello', function(x){console.log(x)});
reqrep2.send('hello', function(x){
    console.log(x + 'sdf');
    console.log(x + 'sfsf');
});
*/

sub = context.Socket(zmq.SUB);
sub.connect("tcp://127.0.0.1:10000", {'username':'hugo'});
sub.onmessage = function(x){
	console.log(['10000', x]);
	var d = jQuery.parseJSON( x );

	var redis = d.middleware['redis']
	var s = "Redis-1[" + redis[0]['hostname'] + "], Status[";
	if(redis[0]['status'] == false) { 
		s += "<font color='red'>Down</font>]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;";
	} else {
		s += "<font color='blue'>Live</font>]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;"; 
	}
	
	s += "Redis-2[" + redis[1]['hostname'] + "], Status[";
	if(redis[1]['status'] == false) { 
		s += "<font color='red'>Down</font>]";
	} else {
		s += "<font color='blue'>Live</font>]"; 
	}

    $('#redis_box').html( s );

    var rmq = d.middleware['rabbitmq']
	var s = "Rabbitmq-1[" + rmq[0]['hostname'] + "] Status[";
	if(rmq[0]['status'] == false) { 
		s += "<font color='red'>Down</font>]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;";
	} else {
		s += "<font color='blue'>Live</font>]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;"; 
	}
	
	s += "Rabbitmq-2[" + rmq[1]['hostname'] + "] Status[";
	if(rmq[1]['status'] == false) { 
		s += "<font color='red'>Down</font>]";
	} else {
		s += "<font color='blue'>Live</font>]"; 
	}

    $('#rabbitmq_box').html( s );
}

sub = context.Socket(zmq.SUB);
sub.connect("tcp://127.0.0.1:10002", {'username':'hugo'});
sub.onmessage = function(x){
	console.log(['10002', x]);
    $('#state_box').text(x);
}

sub2 = context.Socket(zmq.SUB);
sub2.connect("tcp://127.0.0.1:10003", {'username':'hugo'});
sub2.onmessage = function(x){ 
	console.log(['10003', x]); 
	$('#class_box').text(x);
	//reqrep.send('IDENT ' + rep.identity, function(x){console.log(x)});
}

sub3 = context.Socket(zmq.SUB);
sub3.connect("tcp://127.0.0.1:10004", {'username':'hugo'});
sub3.onmessage = function(x){ 
	console.log(['10004', x]); 
	$('#data_box').text(x);
	//reqrep.send('IDENT ' + rep.identity, function(x){console.log(x)});
}

sub4 = context.Socket(zmq.SUB);
sub4.connect("tcp://127.0.0.1:10005", {'username':'hugo'});
sub4.onmessage = function(x){ 
	console.log(['10005', x]);
	var d = jQuery.parseJSON( x );

	if ( d.process['0']['service'] == 'state')
	{
		$('#state_status').html( x );
	}
	else
	{
		$('#class_status').html( x );
	}
	

	//reqrep.send('IDENT ' + rep.identity, function(x){console.log(x)});
}
/*
rep = context.Socket(zmq.REP);

reqrep.send('IDENT ' + rep.identity, function(x){console.log(x)});
rep.connect("tcp://127.0.0.1:10004", {'username' : 'hugo'});
rep.onmessage = function(x){
	console.log(['10004', x]);
	$('#holder_3').html(x);
//     //echo
	rep.send(x)
}
*/

RPC = function(socket){
    zmq.RPCServer.call(this, socket);
}
RPC.prototype = new zmq.RPCServer();

RPC.prototype.echo = function(arg){
    return arg;
}

//var rpc = new RPC(rep);
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
sub.connect("tcp://127.0.0.1:10002", {'username':'hugo'});
sub.onmessage = function(x){
	//console.log(['10002', x]);
    $('#holder_1').html(x);
}

sub2 = context.Socket(zmq.SUB);
sub2.connect("tcp://127.0.0.1:10003", {'username':'hugo'});
sub2.onmessage = function(x){ 
	//console.log(['10003', x]); 
	 $('#holder_2').html(x);
	 reqrep.send('IDENT ' + rep.identity, function(x){console.log(x)});
}


rep = context.Socket(zmq.REP);
reqrep.send('IDENT ' + rep.identity, function(x){console.log(x)});
rep.connect("tcp://127.0.0.1:10004", {'username' : 'hugo'});
rep.onmessage = function(x){
	console.log(['10004', x]);
	$('#holder_3').html(x);
//     //echo
	rep.send(x)
}


RPC = function(socket){
    zmq.RPCServer.call(this, socket);
}
RPC.prototype = new zmq.RPCServer();

RPC.prototype.echo = function(arg){
    return arg;
}

var rpc = new RPC(rep);
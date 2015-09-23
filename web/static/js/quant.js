$(function() {
    // Open up a connection to our server
    var a = {'process':{
        '0': {'ipaddress': '172.31.7.217', 'pid_type': 'parent', 'pid': '8279', 'live':true, 'service': 'state'}, 
        '8289': {'pid_type': 'child', 'live':true}, 
        '8290': {'pid_type': 'child', 'live':true}}
    };

    var b = {'process':{
        0: {'ipaddress': '172.31.7.217', 'pid_type': 'parent', 'pid':8279, 'live': true, 'service': 'state'}, 
        8289: {'pid_type': 'child', 'live': true}, 
        8290: {'pid_type': 'child', 'live': true}}
    };

    /*
    var b = [{"process":{"id":"1","tagName":"apple"},
    {"id":"2","tagName":"orange"},
    {"id":"3","tagName":"banana"},
    {"id":"4","tagName":"watermelon"},
    {"id":"5","tagName":"pineapple"}}];


    var c = [{"id":"1","tagName":"apple"},
    {"id":"2","tagName":"orange"},
    {"id":"3","tagName":"banana"},
    {"id":"4","tagName":"watermelon"},
    {"id":"5","tagName":"pineapple"}];
    */

    //var d = {'process':{'0':{'test1':'test11'}, '1':{'test2':'test222'}}};
    
    //$('#state_status').html( b.process[0]['ipaddress'] );
    //return;
    var socket = io.connect("", {'host': '52.68.73.241', 'port': 9999});

    // Save our plot placeholder 
    
    var $placeholder = $('#state_status'); 
    // Maximum # of data points to plot 
    var datalen = 100; 
    // This will be the plot object 
    var plot = null; 
    // Set up some options on our data series 
    var series = { 
        label: "Value", 
        lines: { 
            show: true, 
            fill: true 
        }, 
        points: { 
            show:true 
        }, 
        data: [] 
    
    }; 

    // What do we do when we get a message? 
    socket.on('message', function(msg) {
        
        //alert( msg.toString() );
        //return;
        //var d = $.parseJSON(msg);
        var d = jQuery.parseJSON( msg )

        if( d.process['0']['service'] == 'state')
        {
            $('#state_status').html( msg );
        }
        else
        {
            $('#class_status').html( msg );
        }
        
    });

    // Just update our conn_status field with the connection status 
    socket.on('connect', function() { 
        $('#conn_status').html('<b>Connected</b>'); 
	// this is the call that streams the sine wave data
	socket.emit('stream', '');
    });
    socket.on('error', function() { 
        $('#conn_status').html('<b>Error</b>'); 
    });
    socket.on('disconnect', function() { 
        $('#conn_status').html('<b>Closed</b>'); 
    });
}); 
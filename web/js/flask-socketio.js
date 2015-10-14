var socket = null;
var broadcast_data = null;
var namespace = '/quant'; // change to an empty string to use the global namespace
var port = '5000'

$(document).ready(function(){
    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    console.log(['socket', 'http://' + document.domain + ':' + port + namespace ]);
    //var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket = io.connect('http://' + document.domain + ':' + port + namespace);
    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
    });

    // event handler for server sent data
    // the data is displayed in the "Received" section of the page

    /* Data Result Response */
    socket.on('data_response', function(msg) {
        if( msg.qkey == $('#service_data').val()){
            if( msg.data != 1) {
                $('#data_box').html( msg.data.replace(msg.qkey, "<font color='blue'>" + msg.qkey + "</font>") );
            }
        }
    });

    /* State Result Response */
    socket.on('state_response', function(msg) {
        if( msg.qkey == $('#service_data').val()) {
            if( msg.data != 1) {
                $('#state_box').html( msg.data.replace(msg.qkey, "<font color='blue'>" + msg.qkey + "</font>") );
            }
        }
    });

    /* Class Result Response */
    socket.on('class_response', function(msg) {
        if( msg.qkey == $('#service_data').val()) {
            if( msg.data != 1) {
                $('#class_box').html( msg.data.replace(msg.qkey, "<font color='blue'>" + msg.qkey + "</font>") );
            }
        }
    });

    socket.on('service_state', function(msg) {
        var d = jQuery.parseJSON( msg.data );

        /* Redis Status Start */
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
        /* Redis Status End */

        /* Rabbit Status Start */
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
        /* Rabbit Status End */

        /* Serive Status Start */
        t = d.process['0']['service'].toUpperCase() + ": " + d.process['0']['ipaddress'] + ", ";
        for( var i = 0; i < Object.keys(d.process).length; i++ )
        {
            t += "PId :" + d.process[i]['pid'] + ", Live:";
            if( d.process[i]['live'] == 'live' )
            {
                t += "<font color='blue'>Live</font>";  
            } else {
                t += "<font color='red'>Down</font>";
            }

            t += ", Type:" + d.process[i]['process_type'];
            if( i != (Object.keys(d.process).length -1) )
            {
                t += ", ";
            }
        }

        if ( d.process['0']['service'] == 'state')
        {
            $('#state_status').html( t );
        }
        else if( d.process['0']['service'] == 'class' )
        {
            $('#class_status').html( t );
        }
        else if( d.process['0']['service'] == 'data' )
        {
            $('#data_status').html( t );
        }
        t = ""

    });

});

var send = function() {
    socket.emit('service state', {data: $('#service_data').val()});
    broadcast_data = $('#service_data').val();
    return false;
};
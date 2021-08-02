<script type="text/javascript" src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js"></script>
<script type="text/javascript" charset="utf-8">
  $(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // listen for mqtt_message events
    // when a new message is received, log and append the data to the page
    socket.on('mqtt_message', function(data) {
      console.log(data);
      var text = '(' + data['topic'] + ' qos: ' + data['qos'] + ') ' + data['payload'];
      $('#subscribe_messages').append(text + '<br><br>');
    })
  });
</script>

<div id="subscribe_messages"></div>
const socket = new WebSocket('ws://localhost:5000/');

gamepad.on('move', 'leftStick', function(event) {
    // Send joystick values as a WebSocket message
    socket.send(JSON.stringify({
      x: event.value.x,
      y: event.value.y
    }));
  });
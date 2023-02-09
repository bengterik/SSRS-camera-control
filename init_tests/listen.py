from pymavlink import mavutil

# Start a connection listening on port 14445 where QGC forwards messages
the_connection = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)

the_connection.wait_heartbeat()

while(True):
    msg = the_connection.recv_match(type='SERVO_OUTPUT_RAW',blocking=True)
    # print the three servo values
    print('Servos 1:', msg.servo1_raw, '\t2:', msg.servo2_raw, '\t3:', msg.servo3_raw)
from pymavlink import mavutil

# Start a connection listening on port 14445 where QGC forwards messages
the_connection = mavutil.mavlink_connection('localhost:14445', baud=57600)

print("Waiting for heartbeat")


while(True):
    msg = the_connection.recv_match(blocking=True)
    print(msg)
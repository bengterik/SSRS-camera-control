from pymavlink import mavutil

# Start a connection listening on port 14445 where QGC forwards messages
the_connection = mavutil.mavlink_connection('130.235.202.14:14550', source_system=2)

while(True):
    msg = the_connection.recv_match(blocking=True)
    # print the three servo values
    print(msg)
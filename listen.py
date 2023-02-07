from pymavlink import mavutil

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('localhost:14445', baud=57600)

print("Waiting for heartbeat")


while(True):
    msg = the_connection.recv_match(blocking=True)
    print(msg)
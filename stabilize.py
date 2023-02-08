import time
from pymavlink import mavutil

def send(command, param1, param2, param3, param4, param5, param6, param7):
    print("Sending command: %s" % command)
    
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, 
                                         command, 0, param1, param2, param3, param4, param5, param6, param7)

    msg = the_connection.recv_match(type='COMMAND_ACK',blocking=True, timeout=1)
    
    if not msg:
        print("No response")

    print(msg)

# Start a connection listening on port 14445 where QGC forwards messages
the_connection = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600)

the_connection.wait_heartbeat()
print("Heartbeat received")

send(mavutil.mavlink.MAV_CMD_DO_MOUNT_CONFIGURE, 2, 1, 1, 1, 0, 0, 0)

send(mavutil.mavlink.MAV_CMD_DO_MOUNT_CONTROL, 0, 0, 0, 0, 0, 0, 2)

def test_all(): 
    for i in range(-90, 90):
        send(mavutil.mavlink.MAV_CMD_DO_MOUNT_CONTROL, 0, 0, i, 0, 0, 0, 2)

    time.sleep(1)

    for i in range(-90, 90):
        send(mavutil.mavlink.MAV_CMD_DO_MOUNT_CONTROL, 0, i, 0, 0, 0, 0, 2)

    time.sleep(1)

    for i in range(-90, 90):
        send(mavutil.mavlink.MAV_CMD_DO_MOUNT_CONTROL, i, 0, 0, 0, 0, 0, 2)

test_all()
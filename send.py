from pymavlink import mavutil

# Start a connection listening on port 14445 where QGC forwards messages
the_connection = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)

the_connection.wait_heartbeat()

the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_DO_MOUNT_CONTROL, 0, 0, 0, 0, 0, 0, 0, 1)

msg = the_connection.recv_match(type='COMMAND_ACK',blocking=True)
print(msg)
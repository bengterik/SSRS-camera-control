from pymavlink import mavutil
import os

# Set MAVLink protocol to 2.0
os.environ["MAVLINK20"] = "1"

print("Starting connection")

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)

print("Waiting for heartbeat")

msg = the_connection.recv_match(blocking=True)

while(True):
    the_connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))
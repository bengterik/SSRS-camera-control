print("Start simulator (SITL)")

# Workaround for backwards-compatibility
import sys
import time

import dronekit_sitl

sitl = dronekit_sitl.start_default()
connection_string = '/dev/ttyUSB0'

# Import DroneKit-Python
from dronekit import connect, VehicleMode

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, baud=57600) # , wait_ready=True

# Get some vehicle attributes (state)
print("Get some vehicle attribute values:")
print(" GPS: %s" % vehicle.gps_0)
print(" Battery: %s" % vehicle.battery)
print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
print(" Is Armable?: %s" % vehicle.is_armable)
print(" System status: %s" % vehicle.system_status.state)
print(" Mode: %s" % vehicle.mode.name)    # settable
print("Gimbal status: %s" % vehicle.gimbal)

time.sleep(10)
while(True):
    vehicle.gimbal.rotate(0, 0, 0)
    time.sleep(1)
    vehicle.gimbal.rotate(-35, -8, -40)
    time.sleep(1)

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
sitl.stop()
print("Completed")
from pymavlink import mavutil

baud = 57600
port = '/dev/ttyACM0'

class Connection:
    def __init__(self):
        self.the_connection = mavutil.mavlink_connection(port, baud=baud)

        self.the_connection.wait_heartbeat()

        print("Heartbeat received")

    def send(self, command, param1, param2, param3, param4, param5, param6, param7):
        print("Sending command: %s" % command)
        
        self.the_connection.mav.command_long_send(self.the_connection.target_system, self.the_connection.target_component, 
                                            command, 0, param1, param2, param3, param4, param5, param6, param7)

        msg = self.the_connection.recv_match(type='COMMAND_ACK',blocking=False, timeout=1)
        
        print(msg)
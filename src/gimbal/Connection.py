from pymavlink import mavutil

DEBUG = True

SIMULATOR = 'tcp:127.0.0.1:5762'
SERIAL = '/dev/ttyACM0'

BAUD_RATE = 57600
PORT = SIMULATOR
REQUEST_TIMEOUT = 1 # seconds

class Connection:
    def __init__(self):
        if DEBUG: print("Connecting to %s at %s baud" % (PORT, BAUD_RATE))
        self.the_connection = mavutil.mavlink_connection(PORT, baud=BAUD_RATE)
        self.parameters = {}
        self.the_connection.wait_heartbeat()

        print("Heartbeat received")

    def read_gimbal_servos(self):
        msg = self.the_connection.recv_match(type='SERVO_OUTPUT_RAW',blocking=True)

        return (msg.servo4_raw, msg.servo5_raw, msg.servo6_raw)

    def send(self, command, param1, param2, param3, param4, param5, param6, param7):
        print("Sending command: %s" % command)
        
        self.the_connection.mav.command_long_send(self.the_connection.target_system, self.the_connection.target_component, 
                                            command, 0, param1, param2, param3, param4, param5, param6, param7)

        msg = self.the_connection.recv_match(type='COMMAND_ACK',blocking=True, timeout=1)
        
        print(msg)

    def send_pitch_yaw(self, pitch, yaw):
        "Set pitch and yaw with stabilization in all axes"
        self.send(mavutil.mavlink.MAV_CMD_DO_GIMBAL_MANAGER_PITCHYAW, pitch, yaw, 0, 0, 4+8+16, 0, 0)
    
    def request_parameters(self):
        "Requests all parameters from the vehicle and puts them in a dictionary"
        
        print("Requesting parameters...")

        self.the_connection.mav.param_request_list_send(self.the_connection.target_system, self.the_connection.target_component)
                
        while True:
            try:       
                # Since number of parameters is unknown, we request until a certain timeout is reached
                param = self.the_connection.recv_match(type='PARAM_VALUE', blocking=True, timeout=REQUEST_TIMEOUT).to_dict()
                
                if DEBUG: print('name: %s\tvalue: %d' % (message['param_id'], message['param_value']))
                
                self.parameters |= {param['param_id']: param['param_value']}
            
            except Exception as error:
                break
        
        print("%d parameters received" % len(self.parameters))

    def request_parameter(self, parameter):
        "Requests a single parameter from the vehicle and returns it"
        
        print("Requesting parameter %s..." % parameter)
        self.the_connection.mav.param_request_read_send(
            self.the_connection.target_system, self.the_connection.target_component, parameter, -1)
        try:       
            # Since number of parameters is unknown, we request until a certain timeout is reached
            param = self.the_connection.recv_match(type='PARAM_VALUE', blocking=True, timeout=REQUEST_TIMEOUT).to_dict()
            
            if DEBUG: print('name: %s\tvalue: %d' % (message['param_id'], message['param_value']))
            
            return param['param_value']
        
        except Exception as error:
            return None
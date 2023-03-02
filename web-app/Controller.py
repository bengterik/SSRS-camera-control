import time
import Connection
from HandController import HandController
# Software limits to saturate keyboard input (DOES NOT AFFECT HARDWARE LIMITS)
YAW_MIN = -240
YAW_MAX = -116
YAW_NEUTRAL = -168
YAW_RETRACTED = YAW_MIN
PITCH_MIN = -20
PITCH_MAX = 30
PITCH_NEUTRAL = 6
PITCH_RETRACTED = 6

DEGREE_PER_KEY_PRESS = 1

class Controller:
    def __init__(self, input_device):
        self.controller = input_device
        self.connection = Connection.Connection()

        self.pitch = PITCH_NEUTRAL # neutral pitch
        self.yaw = YAW_NEUTRAL # neutral yaw
        self.rate = 12 # degrees per key press

        self.last_pos = (self.pitch, self.yaw)

    def add_sat(self, value, change, min, max):
            if value <= min:
                return min 
            elif value >= max:
                return max
            else:
                return value + change

    def update_position(self, pitch, yaw):
        new_pos = (self.add_sat(self.pitch, pitch, PITCH_MIN, PITCH_MAX), 
                   self.add_sat(self.yaw, yaw, YAW_MIN, YAW_MAX))

        
        if new_pos != self.last_pos:
            self.connection.gimbal_pitch_yaw(new_pos[0], new_pos[1])
            
            self.last_pos = new_pos
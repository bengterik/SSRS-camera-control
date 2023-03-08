# Software limits to saturate keyboard input (DOES NOT AFFECT HARDWARE LIMITS)
YAW_MIN = -240
YAW_MAX = -116
YAW_NEUTRAL = -168
YAW_RETRACTED = YAW_MIN
PITCH_MIN = -20
PITCH_MAX = 30
PITCH_NEUTRAL = 6
PITCH_RETRACTED = 6

PITCH_SENSITIVITY = 1
YAW_SENSITIVITY = 1

class Controller:
    """
    Holds the state of the gimbal and manages saturation of control input
    """
    def __init__(self, start_pos = (PITCH_NEUTRAL, YAW_NEUTRAL)):
        self.pitch_yaw = start_pos
        print("Controller initialized at position: " + str(self.pitch_yaw))

    def add_sat(self, value, change, min, max):
            new_value = value + change
            if new_value <= min:
                return min 
            elif new_value >= max:
                return max
            else:
                return value + change

    def update_pitch_yaw(self, pitch, yaw):
        new_pitch = self.add_sat(self.pitch_yaw[0], pitch*PITCH_SENSITIVITY, PITCH_MIN, PITCH_MAX) 
        new_yaw = self.add_sat(self.pitch_yaw[1], yaw*YAW_SENSITIVITY, YAW_MIN, YAW_MAX)
        self.pitch_yaw = (new_pitch, new_yaw)

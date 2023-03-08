# Software limits to saturate keyboard input (DOES NOT AFFECT HARDWARE LIMITS)
YAW_MIN = -240
YAW_MAX = -116
YAW_NEUTRAL = -168
YAW_RETRACTED = YAW_MIN
PITCH_MIN = -20
PITCH_MAX = 30
PITCH_NEUTRAL = 6
PITCH_RETRACTED = 6

class Controller:
    """
    Holds the state of the gimbal and manages saturation of control input
    """
    def __init__(self, start_pos = (PITCH_NEUTRAL, YAW_NEUTRAL)):
        self.last_pos = start_pos

    def add_sat(self, value, change, min, max):
            if value <= min:
                return min 
            elif value >= max:
                return max
            else:
                return value + change

    def update_position(self, pitch, yaw):
        new_pitch = self.add_sat(self.last_pos[0], pitch, PITCH_MIN, PITCH_MAX), 
        new_yaw = self.add_sat(self.last_pos[1], yaw, YAW_MIN, YAW_MAX)
        self.last_pos = (new_pitch, new_yaw)

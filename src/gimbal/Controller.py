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
    def __init__(self):
        self.connection = Connection.Connection()
        self.pitch = PITCH_NEUTRAL # neutral pitch
        self.yaw = YAW_NEUTRAL # neutral yaw
        self.rate = 12 # degrees per key press
    
    def add_sat(self, value, change, min, max):
            if value <= min:
                return min 
            elif value >= max:
                return max
            else:
                return value + change

def main():
    controller = HandController()

    while True:
        last_pos = controller.position()
        time.sleep(0.1)
        new_pos = controller.position()
        if new_pos != last_pos:
            print(new_pos)

if __name__ == "__main__":
    main()
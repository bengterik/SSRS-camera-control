import time
import Connection
from pynput import keyboard
from pymavlink import mavutil

# Software limits to saturate keyboard input (DOES NOT AFFECT HARDWARE LIMITS)
YAW_MIN = -50
YAW_MAX = 128
YAW_NEUTRAL = 12
YAW_RETRACTED = YAW_MAX
PITCH_MIN = -20
PITCH_MAX = 30
PITCH_NEUTRAL = 6
PITCH_RETRACTED = 4
DEGREE_PER_KEY_PRESS = 4

class Controller:
    def __init__(self):
        self.connection = Connection.Connection()
        self.pitch = PITCH_NEUTRAL # neutral pitch
        self.yaw = YAW_NEUTRAL # neutral yaw
        self.rate = 12 # degrees per key press
    
    def sat(self, value, change, min, max):
            if value < min:
                return min 
            elif value > max:
                return max
            else:
                return value + change
     
    def on_press(self, key):
        if key == keyboard.Key.up:
            self.pitch = self.sat(self.pitch, DEGREE_PER_KEY_PRESS, PITCH_MIN, PITCH_MAX)
            self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)
    
        elif key == keyboard.Key.down:
            self.pitch = self.sat(self.pitch, -DEGREE_PER_KEY_PRESS, PITCH_MIN, PITCH_MAX)
            self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)
        
        elif key == keyboard.Key.left:
            self.yaw = self.sat(self.yaw, -DEGREE_PER_KEY_PRESS, YAW_MIN, YAW_MAX)
            self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)

        elif key == keyboard.Key.right:
            self.yaw = self.sat(self.yaw, DEGREE_PER_KEY_PRESS, YAW_MIN, YAW_MAX)
            self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)

        elif key.char == 'r':
            self.connection.gimbal_retract()
            self.pitch = PITCH_RETRACTED
            self.yaw = YAW_RETRACTED
            
        elif key.char == 'n':
            self.connection.gimbal_neutral()
            self.pitch = PITCH_NEUTRAL
            self.yaw = YAW_NEUTRAL

        elif key == keyboard.Key.esc:
            # Stop listener
            return False
        
        print("pitch: %s, yaw: %s" % (self.pitch, self.yaw))
        

       
    def activate_gimbal_control_keys(self):
        
        listener = keyboard.Listener(
            on_press=self.on_press)
        listener.start()

        # Configure for MAVLink targetting mode and stabilization
        #self.connection.send(mavutil.mavlink.MAV_CMD_DO_MOUNT_CONFIGURE, 2, 0, 0, 0, 0, 0, 0)

        # Send "natural" pitch and yaw
        #self.connection.send_pitch_yaw(self.pitch, self.yaw)

def main():
    controller = Controller()
    
    controller.activate_gimbal_control_keys()

    while True:
        time.sleep(1)
        #servos = controller.connection.read_gimbal_servos()
        #print("servos: %s" % str(servos))
        #print("pitch: %s, yaw: %s" % (controller.pitch, controller.yaw))
        #print("yaw: %s, pitch: %s, roll: %s, " % (yaw, pitch, roll))


if __name__ == "__main__":
    main()
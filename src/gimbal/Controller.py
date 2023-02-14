import time
import Connection
from pynput import keyboard
from pymavlink import mavutil

# Software limits to saturate keyboard input (DOES NOT AFFECT HARDWARE LIMITS)
YAW_MIN = -50
YAW_MAX = 120
PITCH_MIN = -20
PITCH_MAX = 30

class Controller:
    def __init__(self):
        self.connection = Connection.Connection()
        self.pitch = 6 # neutral pitch
        self.yaw = 12 # neutral yaw
        self.rate = 4 # degrees per key press

    def on_press(self, key):
        if key == keyboard.Key.up:
            self.pitch += self.rate
            if self.pitch > PITCH_MAX:
                self.pitch = PITCH_MAX
        elif key == keyboard.Key.down:
            self.pitch -= self.rate
            if self.pitch < PITCH_MIN:
                self.pitch = PITCH_MIN
        elif key == keyboard.Key.left:
            self.yaw -= self.rate
            if self.yaw < YAW_MIN:
                self.yaw = YAW_MIN
        elif key == keyboard.Key.right:
            self.yaw += self.rate
            if self.yaw > YAW_MAX:
                self.yaw = YAW_MAX
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        
        print("pitch: %s, yaw: %s" % (self.pitch, self.yaw))
        
        self.connection.send_pitch_yaw(self.pitch, self.yaw)

    # enter two angles in the terminal and send them to the gimbal
    def gimbal_control_keys(self):
        
        listener = keyboard.Listener(
            on_press=self.on_press)
        listener.start()

        # Configure for MAVLink targetting mode and stabilization
        self.connection.send(mavutil.mavlink.MAV_CMD_DO_MOUNT_CONFIGURE, 2, 0, 0, 0, 0, 0, 0)

        # Send "natural" pitch and yaw
        self.connection.send_pitch_yaw(self.pitch, self.yaw)
        
        while True:
            time.sleep(1)

def main():
    controller = Controller()
    
    controller.gimbal_control_keys()
    #print(controller.connection.request_parameter(b'SERVO9_MIN'))

if __name__ == "__main__":
    main()
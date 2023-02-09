import time
import Connection
from pynput import keyboard
from pymavlink import mavutil


class Controller:
    def __init__(self):
        self.connection = Connection.Connection()
        self.pitch = -31 # neutral pitch
        self.yaw = -57 # neutral yaw
        self.rate = 1
    

    def on_press(self, key):
        if key == keyboard.Key.up:
            self.pitch += self.rate
            if self.pitch > 18:
                self.pitch = 18
        elif key == keyboard.Key.down:
            self.pitch -= self.rate
            if self.pitch < -86:
                self.pitch = -86
        elif key == keyboard.Key.right:
            self.yaw -= self.rate
            if self.yaw < -175:
                self.yaw = -175
        elif key == keyboard.Key.left:
            self.yaw += self.rate
            if self.yaw > 175:
                self.yaw = 175
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        
        print("pitch: %s, yaw: %s" % (self.pitch, self.yaw))
        
        self.connection.send_pitch_yaw(self.pitch, self.yaw)

    # enter two angles in the terminal and send them to the gimbal
    def control_loop(self):
        
        listener = keyboard.Listener(
            on_press=self.on_press)
        listener.start()

        # Configure for MAVLink targetting mode and stabilization
        self.connection.send(mavutil.mavlink.MAV_CMD_DO_MOUNT_CONFIGURE, 2, 1, 1, 1, 0, 0, 0)

        # Send "natural" pitch and yaw
        self.connection.send_pitch_yaw(self.pitch, self.yaw)
        
        while True:
            time.sleep(1)

def main():
    controller = Controller()
    controller.control_loop()

if __name__ == "__main__":
    main()
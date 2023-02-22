import time
import Connection
import evdev
import asyncio
from evdev import InputDevice, categorize, ecodes
from pynput import keyboard
from pymavlink import mavutil

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
     
    def on_press(self, key):
        try:
            if key == keyboard.Key.up:
                self.pitch = self.add_sat(self.pitch, DEGREE_PER_KEY_PRESS, PITCH_MIN, PITCH_MAX)
                self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)
    
            elif key == keyboard.Key.down:
                self.pitch = self.add_sat(self.pitch, -DEGREE_PER_KEY_PRESS, PITCH_MIN, PITCH_MAX)
                self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)
            
            elif key == keyboard.Key.left:
                self.yaw = self.add_sat(self.yaw, -DEGREE_PER_KEY_PRESS, YAW_MIN, YAW_MAX)
                self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)

            elif key == keyboard.Key.right:
                self.yaw = self.add_sat(self.yaw, DEGREE_PER_KEY_PRESS, YAW_MIN, YAW_MAX)
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
            
        except AttributeError:
            print('special key {0} pressed'.format(
                key))
        
        print("pitch: %s, yaw: %s" % (self.pitch, self.yaw))
   
    def activate_gimbal_control_keys(self):
        
        listener = keyboard.Listener(
            on_press=self.on_press)
        
        listener.start()
        
        print("Keyboard control activated. Press ESC to exit.")

        # Configure for MAVLink targetting mode and stabilization
        #self.connection.send(mavutil.mavlink.MAV_CMD_DO_MOUNT_CONFIGURE, 2, 0, 0, 0, 0, 0, 0)

        # Send "natural" pitch and yaw
        #self.connection.send_pitch_yaw(self.pitch, self.yaw)


    async def game_controller_listener(self, dev):
        async for ev in dev.async_read_loop():
            if ev.code == 3:
                stick_value = ev.value

                # Filters out noise
                if stick_value > 130:
                    dir = 1
                elif stick_value < 120:
                    dir = -1
                else:
                    dir = 0
                
                if dir != 0:
                    print("Vertical %d" % ev.value)
                    self.pitch = self.add_sat(self.pitch, dir, PITCH_MIN, PITCH_MAX)
                    self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)

            elif ev.code == 4:
                stick_value = ev.value

                # Filters out noise
                if stick_value > 130:
                    dir = 1
                elif stick_value < 120:
                    dir = -1
                else:
                    dir = 0
                
                if dir != 0:
                    print("Horizontal %d" % ev.value)
                    self.yaw = self.add_sat(self.yaw, dir, YAW_MIN, YAW_MAX)
                    self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)

            elif ev.code == 16:
                self.yaw = self.add_sat(self.yaw, ev.value, YAW_MIN, YAW_MAX)
                self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)

            elif ev.code == 17:
                self.pitch = self.add_sat(self.pitch, -ev.value, PITCH_MIN, PITCH_MAX) # value inverted
                self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)
            
        #sprint(repr(ev))

def main():
    controller = Controller()

    #controller.activate_gimbal_control_keys()
    print("loading devices")
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    
    for device in devices:
       print(device.path, device.name, device.phys)
    
    dev = InputDevice('/dev/input/event15')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(controller.game_controller_listener(dev))

    while True:
        time.sleep(1)
        #servos = controller.connection.read_gimbal_servos()
        #print("servos: %s" % str(servos))
        #print("pitch: %s, yaw: %s" % (controller.pitch, controller.yaw))
        #print("yaw: %s, pitch: %s, roll: %s, " % (yaw, pitch, roll))


if __name__ == "__main__":
    main()
from threading import Thread
import time
import asyncio
from collections import deque
import evdev
from evdev import InputDevice, categorize, ecodes

class ControllerThread(Thread):

    def __init__(self, loop, DPAD_deque, RST_deque):
        Thread.__init__(self, daemon=True)
        self.loop = loop
        self.DPAD_deque = DPAD_deque
        self.RST_deque = RST_deque

        self.RST_horiz = 127 # RST = Right Stick
        self.RST_vert = 127
        
        self.DPAD_horiz = 0 # DPAD = arrow keys on controller
        self.DPAD_vert = 0

        self.dev = InputDevice('/dev/input/event15')
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        
        print("Device(s):")
        for device in devices:
            print(device.path, device.name, device.phys)

    async def game_controller_listener(self, dev):
        async for ev in dev.async_read_loop():
            if ev.code == 3:
                self.RST_horiz = ev.value

            elif ev.code == 4:
                self.RST_vert = ev.value 

            elif ev.code == 16:
                self.DPAD_horiz += ev.value

            elif ev.code == 17:
                self.DPAD_vert += ev.value 

            if ev.code == 3 or ev.code == 4: # Joystick input
                self.RST_deque.appendleft(self.joystick_position()) 
            elif ev.code == 16 or ev.code == 17: # D-Pad input
                self.DPAD_deque.appendleft(self.DPAD_position())
        
    
    def joystick_position(self):
        return(self.RST_vert, self.RST_horiz)
    
    def DPAD_position(self):
        temp = (self.DPAD_vert, self.DPAD_horiz)
        self.DPAD_horiz = 0
        self.DPAD_vert = 0
        return temp
        
    def run(self):
        self.loop.run_until_complete(self.game_controller_listener(self.dev))


JOYSTICK_YAW_SENSITIVITY = 0.01
JOYSTICK_PITCH_SENSITIVITY = 0.01

JOYSTICK_NOISE_THRESHOLD = 1

class Controller:
    def __init__(self):
        self.pitch = 0
        self.yaw = 0
        self.DPAD_deque = deque(maxlen=10) 
        self.RST_deque = deque(maxlen=1) # Last value only interesting
        
        self.controller_t = ControllerThread(asyncio.get_event_loop(), self.DPAD_deque, self.RST_deque)
        self.controller_t.start()

    def scale(self, value):
        scaled = value - 127

        if abs(scaled) > JOYSTICK_NOISE_THRESHOLD:
            return scaled
        else:
            return 0
    
    def joystick_read(self):
        try:
            vert, horiz = self.RST_deque[0] # Only peek the queue as we don't want to loose the last value
        except IndexError:
            vert, horiz = 127, 127

        self.pitch -= round(self.scale(vert)*JOYSTICK_PITCH_SENSITIVITY) # inverted on controller
        self.yaw += round(self.scale(horiz)*JOYSTICK_YAW_SENSITIVITY)
    
    def DPAD_read(self):
        
        # Take all D-Pad inputs and add them together
        for _ in range(len(self.DPAD_deque)):
            vert, horiz = self.DPAD_deque.pop()
            self.pitch -= vert # inverted on controller
            self.yaw += horiz
    
    def position(self):
        self.joystick_read()
        self.DPAD_read()
        return (self.pitch, self.yaw)

def main():
    controller = Controller()
    
    while True:
        last_pos = controller.position()
        time.sleep(0.1)
        new_pos = controller.position()
        if new_pos != last_pos:
            print(new_pos)
        
if __name__ == "__main__":
    main()
from threading import Thread
import time
import asyncio
import evdev
from evdev import InputDevice, categorize, ecodes

class ControllerThread(Thread):

    def __init__(self, loop):
        Thread.__init__(self, daemon=True)
        self.loop = loop
        self.horiz = 127
        self.vert = 127
        self.dev = InputDevice('/dev/input/event15')
        
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        
        print("Device(s):")
        for device in devices:
            print(device.path, device.name, device.phys)

    async def game_controller_listener(self, dev):
        async for ev in dev.async_read_loop():
            #print("Horiz: %s, Vert: %s" % (self.horiz, self.vert))
            if ev.code == 4:
                self.horiz = ev.value

            elif ev.code == 3:
                self.vert = ev.value 

            elif ev.code == 16:
                self.vert += 1

            elif ev.code == 17:
                self.horiz += 1
    
    def position(self):
        return (self.horiz, self.vert)
        
    def run(self):
        self.loop.run_until_complete(self.game_controller_listener(self.dev))


JOYSTICK_SENSITIVITY = 0.01
JOYSTICK_NOISE_THRESHOLD = 1

class Controller:
    def __init__(self):
        self.pitch = 0
        self.yaw = 0
        
        self.controller_t = ControllerThread(asyncio.get_event_loop())
        self.controller_t.start() 


    def tune(self, value):
        scaled = value - 127

        if abs(scaled) > JOYSTICK_NOISE_THRESHOLD:
            return scaled * JOYSTICK_SENSITIVITY
        else:
            return 0
    
    def position(self):
        self.pitch += round(self.tune(self.controller_t.vert))
        self.yaw += round(self.tune(self.controller_t.horiz))
        return (self.pitch, self.yaw)

def main():
    controller = Controller()
    
    while True:
        last_pos = controller.position()
        time.sleep(0.1)
        if controller.position() != last_pos:
            print(controller.position())

if __name__ == "__main__":
    main()
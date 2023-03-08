import time
import threading
from Controller import Controller
from Connection import Connection

class ControllThread:
    def __init__(self):
        self.controller = Controller()
        self.connection = Connection()
        self.last_pitch_yaw = (0, 0)
        
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            pitch, yaw = self.controller.pitch_yaw
            if((pitch, yaw) != self.last_pitch_yaw):
                self.connection.gimbal_pitch_yaw(pitch, yaw)
                self.last_pitch_yaw = (pitch, yaw)        
            time.sleep(0.05)

    def update_position(self, yaw, pitch):
        self.controller.update_pitch_yaw(pitch, yaw)
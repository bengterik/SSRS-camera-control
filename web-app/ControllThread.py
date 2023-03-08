import time
import threading
from Controller import Controller
from Connection import Connection

class ControllThread:
    def __init__(self):
        self.controller = Controller()
        self.connection = Connection()
        self.x = 0
        self.y = 0
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            print('Hello from thread')
            time.sleep(1)

    def update_position(self, x, y):

        self.controller.update_position(x, y)
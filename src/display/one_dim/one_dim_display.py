import time 
from threading import Thread
from queue import PriorityQueue
import constants as constants
from rpi_ws281x import Color, PixelStrip, ws

class OneDimDisplay(Thread):
    def __init__(self, p_q_frame, p_strip):
        Thread.__init__(self)
        self.q_frame = p_q_frame
        self.strip = p_strip
    
    def __del__(self):
        print("Goodbye one dimension !")

    # Receive frame
    def run(self):
        print('Started one dimension display thread')
        #time.sleep(constants.TH_PRIORITY_HIGH)
        while True:
            next_frame = None
            while not self.q_frame.empty():
                next_frame = self.q_frame.get()            
                self.process_frame(next_frame)

    def process_frame(self, next_frame):
        #print("> Receiving frame")
        frame = [None] * len(next_frame)
        for i, row in enumerate(next_frame):
            if type(row).__name__ == 'tuple' or type(row).__name__ == 'NoneType':
                frame[i] = row
            else:
                for j, column in enumerate(row):
                    if column != None or j == len(row)-1:
                        frame[i] = column
                        break
        self.display_frame(frame)
    
    def display_frame(self, frame):
        #print("> Displaying frame")
        for i, led in enumerate(frame):
            if led != None:
                if len(led) == 4:
                    self.strip.setPixelColor(i, Color(led[0], led[1], led[2], led[3]))
                else:    
                    self.strip.setPixelColor(i, Color(led[0], led[1], led[2], 0))
        self.strip.show()
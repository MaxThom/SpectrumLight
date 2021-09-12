import time 
from threading import Thread
from queue import PriorityQueue
import constants as constants
import process.constants as anim_constants
from animations.one_dim_anim import OneDimAnim
from rpi_ws281x import Color, PixelStrip, ws

class OneDimProcess(Thread):
    def __init__(self, p_q_command, p_q_frame, p_strip):
        Thread.__init__(self)
        self.q_frame = p_q_frame
        self.q_command = p_q_command
        self.strip = p_strip
        self.onGoingAnim = []
        self.onGoingThread = []
        self.cancelThread = []
        self.segments = []
    
    def __del__(self):
        print("Goodbye one dimension !")

    # Receive command
    def run(self):
        print('Started one dimension process thread')
        time.sleep(constants.TH_PRIORITY_LOW)
        while True:
            next_cmd = None
            while not self.q_command.empty():
                next_cmd = self.q_command.get()            
                self.process_command(next_cmd)

    def process_command(self, cmd):
        print("> Command " + cmd["command"])
        if cmd["command"] == anim_constants.SEGMENT:
            #self.onGoingAnim = []
            #self.cancelAnim = []
            #self.segments = []
            self.segments.append((cmd["start_index"], cmd["end_index"]))            
            self.onGoingThread.append(None)
            self.cancelThread.append(False)
            self.onGoingAnim.append(OneDimAnim(self.strip, self.q_frame, lambda: self.cancelThread[0], cmd["start_index"], cmd["end_index"]))
        else:
            segment = cmd["segment"]
            if (self.onGoingThread[segment] != None):
                self.cancelThread[segment] = True
                self.onGoingThread[segment].join()
                self.cancelThread[segment] = False
            self.onGoingAnim = Thread(target=self.onGoingAnim[segment].color_wipe, args=((0,0,255), 50))
            self.onGoingAnim.start()
            #time.sleep(3)
            #self.cancelThread[0] = True
 

#commandAnimation = {
#    anim_constants.CLEAR: command_add_wifi,
#    anim_constants.COLOR_WIPE: command_display_networks
#}
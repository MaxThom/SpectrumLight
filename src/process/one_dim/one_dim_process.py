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
            self.command_segment(cmd)            
        elif  cmd["command"] == anim_constants.ANIMATION:
            anim = cmd["name"]
            segment = cmd["segment"]
            config = cmd["configuration"]
            self.join_thread(segment)
            #class_method = getattr(OneDimAnim, "color_wipe")
            #result = class_method(self.onGoingAnim[segment])

            #self.onGoingThread[segment] = Thread(target=self.onGoingAnim[segment].color_wipe, args=((0,0,255), 50))
            #self.onGoingThread[segment] = Thread(target=self.onGoingAnim[segment].rainbow_cycle, args=(0.005,))
            self.onGoingThread[segment] = Thread(target=getattr(self.onGoingAnim[segment], anim), args=(config,))
            self.onGoingThread[segment].start()
            #time.sleep(3)
            #self.cancelThread[0] = True
 
    def command_segment(self, cmd):
        # Join all thread
        self.join_all_threads()
        # Init arrays
        self.onGoingAnim = []
        self.onGoingThread = []
        self.cancelThread = []
        self.segments = []
        # Create segments
        for i, segment in enumerate(cmd["segments"]):
            self.segments.append((segment[0], segment[1]))            
            self.onGoingThread.append(None)
            self.cancelThread.append(False)
            self.onGoingAnim.append(OneDimAnim(self.strip, self.q_frame, lambda: self.cancelThread[i], segment[0], segment[1]))

    def join_all_threads(self):
        for th in self.cancelThread:
            th = True
        for th in self.onGoingThread:
            if (th != None):                
                th.join()
        for th in self.cancelThread:
            th = False

    def join_thread(self, index):
        if (self.onGoingThread[index] != None):
            self.cancelThread[index] = True
            self.onGoingThread[index].join()
            self.cancelThread[index] = False

#commandAnimation = {
#    anim_constants.CLEAR: command_add_wifi,
#    anim_constants.COLOR_WIPE: command_display_networks
#}
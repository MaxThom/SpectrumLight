import time 
from threading import Thread
from queue import PriorityQueue
import constants as constants
import process.constants as anim_constants
from animations.one_dim_anim import OneDimAnim

class OneDimProcess(Thread):
    def __init__(self, p_q_command, p_display):
        Thread.__init__(self)
        self.display = p_display
        self.q_command = p_q_command
        self.onGoingAnim = []
        self.onGoingThread = []
        self.segments = []
    
    def __del__(self):
        print("Goodbye one dimension !")

    # Receive command
    def run(self):
        print('Started one dimension process thread')
        while True:
            next_cmd = None
            while not self.q_command.empty():
                try:
                    next_cmd = self.q_command.get()            
                    self.process_command(next_cmd)
                except Exception as e: 
                    print("Unkown error: " + e)

    def process_command(self, cmd):
        print("> Command " + cmd["command"])
        if cmd["command"] == anim_constants.SEGMENT:
            self.command_segment(cmd)
        elif cmd["command"] == anim_constants.ANIMATION:
            anim = cmd["name"]
            segment = cmd["segment"]
            config = cmd["configuration"]
            if segment >= len(self.onGoingAnim):
                return
            self.join_thread(segment)
            print("TERNATED")            
            self.onGoingThread[segment] = Thread(target=getattr(self.onGoingAnim[segment], anim), args=(config,))
            self.onGoingThread[segment].start()            
 
    def command_segment(self, cmd):
        # Join all thread
        self.join_all_threads()
        print("TERMINATED")
        # Init arrays
        self.onGoingAnim = []
        self.onGoingThread = []
        self.segments = []
        # Create segments
        for i, segment in enumerate(cmd["segments"]):
            self.segments.append((segment[0], segment[1]))            
            self.onGoingThread.append(None)
            self.onGoingAnim.append(OneDimAnim(self.display, (segment[0], segment[1])))

    def join_all_threads(self):
        for th in self.onGoingAnim:
            th.isCancelled = True
        for th in self.onGoingThread:
            if (th != None):                
                th.join()
        for th in self.onGoingAnim:
            th.isCancelled = False

    def join_thread(self, index):
        if (self.onGoingThread[index] != None):
            self.onGoingAnim[index].isCancelled = True
            self.onGoingThread[index].join()
            self.onGoingAnim[index].isCancelled = False

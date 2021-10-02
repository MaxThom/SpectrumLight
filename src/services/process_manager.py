import time 
from threading import Thread, Lock
from queue import PriorityQueue
import constants as constants
from animations.one_dim_anim import OneDimAnim
from animations.two_dim_anim import TwoDimAnim

SEGMENT="segment"
ANIMATION="animation"

class ProcessManagers(Thread):
    def __init__(self, p_q_command, p_display):
        Thread.__init__(self)
        self.display = p_display
        self.q_command = p_q_command
        self.onGoingAnim = []
        self.onGoingThread = []
        self.segments = []
    
    def __del__(self):
        self.join_all_threads()
        print("PROCESS_MANAGER_OUT")

    # Receive command
    def run(self):
        print('Started one dimension process thread')
        while True:
            try:
                next_cmd = None
                while not self.q_command.empty():                
                    next_cmd = self.q_command.get()            
                    self.process_command(next_cmd)
            except Exception as e: 
                print("Unkown error: " + e)

    def process_command(self, cmd):
        print("> Command " + cmd["command"])
        if cmd["command"] == SEGMENT:
            self.command_segment(cmd)
        elif cmd["command"] == ANIMATION:
            anim = cmd["name"]
            segment = cmd["segment"]
            dimension = cmd["dimension"]
            config = cmd["configuration"]
            if segment >= len(self.onGoingAnim):
                return
            next_anim = self.create_animation_for_display(dimension, self.display, self.segments[segment], self.display.anim_mutexes[segment])
            if not hasattr(next_anim, anim):
                print("Animation " + anim + "doest not exist!")
                return
            self.join_thread(segment)
            print("TERNATED")
            self.onGoingAnim[segment] = next_anim
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
        self.display.anim_mutexes = []
        # Create segments
        for i, segment in enumerate(cmd["segments"]):
            self.segments.append(tuple(segment))            
            self.onGoingThread.append(None)
            self.onGoingAnim.append(None)
            self.display.anim_mutexes.append(Lock())

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
    
    def create_animation_for_display(self, dimension, display, segment, mutex):
        if dimension == 1:
            return OneDimAnim(display, segment, mutex)
        elif dimension == 2:
            return TwoDimAnim(display, segment, mutex)
        return None

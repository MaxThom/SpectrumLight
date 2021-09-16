from abc import ABC, abstractmethod
from display.display import __Display

class __Anim(ABC):
    def __init__(self, p_display, p_segment):
        self.display = p_display
        self.segment = p_segment
        self.isCancelled = False       

    def _send_frame(self, frame):
        #print(frame)
        self.display.send_frame(self.start_index, frame)

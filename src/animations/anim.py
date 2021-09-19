from abc import ABC, abstractmethod
from services.display import Display

class __Anim(ABC):
    def __init__(self, p_display, p_segment):
        self.display = p_display
        self.segment = p_segment
        self.isCancelled = False       

    
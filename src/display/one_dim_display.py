import constants as constants
from display.display import __Display
from rpi_ws281x import Color, PixelStrip, ws

class OneDimDisplay(__Display):
    def __init__(self):
        super().__init__()
    
    def __del__(self):
        pass

    def send_frame(self, index, next_frame):        
        try:
            self.__process_frame(index, next_frame)
        except Exception as e: 
            print("Unkown error: " + e)

    def __process_frame(self, index, next_frame):
        frame = None
        if type(next_frame[0]).__name__ == "list":
            frame = [None] * len(next_frame[0])
            for i, row in enumerate(zip(*next_frame)):
                for column in row:
                    if column != None:
                        frame[i] = column
                        break
        else:
            frame = next_frame
        self.__display_frame(index, frame)
    
    def __display_frame(self, index, frame):
        for i, led in enumerate(frame):
            if led != None:
                if len(led) == 4:
                    self.strip.setPixelColor(i+index, Color(led[0], led[1], led[2], led[3]))
                else:    
                    self.strip.setPixelColor(i+index, Color(led[0], led[1], led[2], 0))
        self.strip.show()
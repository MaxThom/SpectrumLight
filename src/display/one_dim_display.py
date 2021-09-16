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
        frame = [None] * len(next_frame)
        for i, row in enumerate(next_frame):
            if type(row).__name__ == 'tuple' or type(row).__name__ == 'NoneType':
                frame[i] = row
            else:
                for j, column in enumerate(row):
                    if column != None or j == len(row)-1:
                        frame[i] = column
                        break
        self.__display_frame(index, frame)
    
    def __display_frame(self, index, frame):
        for i, led in enumerate(frame):
            if led != None:
                if len(led) == 4:
                    self.strip.setPixelColor(i+index, Color(led[0], led[1], led[2], led[3]))
                else:    
                    self.strip.setPixelColor(i+index, Color(led[0], led[1], led[2], 0))
        self.strip.show()
import time 
import threading
import queue
from flask import Flask, request, jsonify
from rpi_ws281x import Color, PixelStrip, ws

from hotspot.hotspot import hotspot_bp
from api.animation_controller import animation_bp, q_command
from display.one_dim.one_dim_display import OneDimDisplay
from process.one_dim.one_dim_process import OneDimProcess
from queue import PriorityQueue
import animation as anim
import constants as constants

class Main:
    def __init__(self):        
        print("Hello world !")
        self.app = Flask(__name__)
        self.app.register_blueprint(hotspot_bp, url_prefix='/')
        self.app.register_blueprint(animation_bp, url_prefix='/api/animation')
        
        self.strip = PixelStrip(constants.LED_COUNT, 
                                constants.LED_PIN, 
                                constants.LED_FREQ_HZ, 
                                constants.LED_DMA, 
                                constants.LED_INVERT, 
                                constants.LED_BRIGHTNESS, 
                                constants.LED_CHANNEL, 
                                constants.LED_STRIP)
        self.strip.begin()

       

        self.q_command = queue.Queue()
        self.q_frame = queue.Queue()
        q_command = self.q_command
        self.process_th = OneDimProcess(self.q_command, self.q_frame, self.strip)
        self.display_th = OneDimDisplay(self.q_frame, self.strip)
        
    
    def __del__(self):
        print("Goodbye wold !")

    def main(self):
        self.display_th.start()
        self.process_th.start()
        
        command = {
            "command": "segment",
            "segments": [
                (0, 17),
                (18, 35),
                (36, 53),
                (54, 71),
                (72, 89),
                (90, 107),
                (108, 125),
                (126, 143)
            ],            
        }
        self.q_command.put(command)
        command = {
            "command": "animation",
            "name": "color_wipe",
            "segment": 0,
            "configuration": {
                "color": (0, 255,0),
                "wait_ms": 50,
                "reverse": True
            }
        }
        self.q_command.put(command)
        command = {
            "command": "animation",
            "name": "rainbow_cycle",
            "segment": 1,
            "configuration": {
                "wait_ms": 50
            }
        }
        self.q_command.put(command)
        command = {
            "command": "animation",
            "name": "color_wipe",
            "segment": 2,
            "configuration": {
                "color": (255, 0, 0),
                "wait_ms": 50,
                "reverse": False
            }
        }
        self.q_command.put(command)
        command = {
            "command": "animation",
            "name": "rainbow_cycle",
            "segment": 3,
            "configuration": {
                "wait_ms": 50
            }
        }
        self.q_command.put(command)
        command = {
            "command": "animation",
            "name": "color_wipe",
            "segment": 4,
            "configuration": {
                "color": (0, 0 ,255),
                "wait_ms": 50,
                "reverse": False
            }
        }
        self.q_command.put(command)
        command = {
            "command": "animation",
            "name": "rainbow_cycle",
            "segment": 5,
            "configuration": {
                "wait_ms": 50
            }
        }
        self.q_command.put(command)
        command = {
            "command": "animation",
            "name": "color_wipe",
            "segment": 6,
            "configuration": {
                "color": (0, 0, 0, 255),
                "wait_ms": 50,
                "reverse": False
            }
        }
        self.q_command.put(command)
        command = {
            "command": "animation",
            "name": "rainbow_cycle",
            "segment": 7,
            "configuration": {
                "wait_ms": 50
            }
        }
        self.q_command.put(command)

     #self.q_frame.put([(0, 0, 0)] * constants.LED_COUNT)
     #for i in range(constants.LED_COUNT):
     #    frame = [None] * constants.LED_COUNT
     #    frame[i] = (0, 0, 255)
     #    self.q_frame.put(frame)
     #    time.sleep(50 / 1000.0)


        self.app.run(host='0.0.0.0', port=80)
        self.display_th.join()

if __name__ == '__main__':
    main = Main()
    main.main()
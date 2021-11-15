import time 
import threading
import queue
from flask import Flask, request, jsonify

from hotspot.hotspot import hotspot_bp
from api.animation_controller import animation_bp, set_dependencies
from services.display import Display
from services.process_manager import ProcessManagers
from queue import PriorityQueue
import constants as constants

class Main:
    def __init__(self):        
        print("Hello world !")
        self.app = Flask(__name__)
        self.app.register_blueprint(hotspot_bp, url_prefix='/')
        self.app.register_blueprint(animation_bp, url_prefix='/api/led')

        self.q_command = queue.Queue()        
        self.display = Display()
        self.process_th = ProcessManagers(self.q_command, self.display)
        set_dependencies(self.q_command, self.display)
    
    def __del__(self):
        print("Goodbye wold !")

    def main(self):
        self.process_th.start()

        # Default animation
        command = {
            "command": "segment",
            "segments": [
                [0, self.display.get_num_pixels()]
            ],            
        }
        self.q_command.put(command)
        command = {
            "command": "animation",
            "name": "off",
            "segment": 0,
            "dimension": 1,
            "configuration": { }
        }
        self.q_command.put(command)
        command = {
            "command": "animation",
            "name": "labyrinth", #rainbow_cycle
            "segment": 0,
            "dimension": 1,
            "configuration": {
                "wait_ms": 0.035,
                "count": 15
            }
        }
        self.q_command.put(command)

        self.app.run(host='0.0.0.0', port=80)
        self.process_th.join()
        self.display_th.join()

if __name__ == '__main__':
    main = Main()
    main.main()

from flask import Blueprint, request, jsonify, render_template
from display.one_dim_display import OneDimDisplay
import queue
import api.constants as constants
import api.utils as utils
import os.path
import subprocess
import pprint


animation_bp = Blueprint('animation', __name__)
q_command = None
display = None

def set_dependencies(p_q_command, p_display):
  global q_command
  global display
  q_command = p_q_command
  display = p_display

@animation_bp.route('/animation/', strict_slashes=False)
def get_animation():
  rtn = {}
  try:
    data = request.get_json()
    pprint.pprint(data)

    if type(data).__name__ == 'dict':
      q_command.put(data)
    else:
      for cmd in data:
        q_command.put(cmd)
        
    rtn["result"] = "Command sent!"
  except Exception as e: 
    print(e)
    rtn["result"] = None
    rtn["err"] = e

  pprint.pprint(rtn)
  return jsonify(rtn)

@animation_bp.route('/brightness/', methods=["POST", "GET"], strict_slashes=False)
def set_brightness():
  rtn = {}
  if request.method == "POST":
    try:
      data = request.get_json()
      pprint.pprint(data)

      if not "brightness" in data or not isinstance(data["brightness"], int) or data["brightness"] < 0 or data["brightness"] > 255:
          raise ValueError

      display.set_brightness(int(data["brightness"]))
      rtn["result"] = f"Brightness set to {data['brightness']}."
    except ValueError:
      rtn["result"] = None
      rtn["err"] = "Brightness must be between 0 and 255."
    except Exception as e: 
      print(e)
      rtn["result"] = None
      rtn["err"] = e
  else:
    try:      
      rtn["brightness"] = display.get_brightness()    
    except Exception as e: 
      print(e)
      rtn["result"] = None
      rtn["err"] = e

  pprint.pprint(rtn)
  return jsonify(rtn)

@animation_bp.route('/configuration/', methods=["POST", "GET"], strict_slashes=False)
def get_config():
  rtn = {}
  if request.method == "POST":
    try:
      data = request.get_json()
      pprint.pprint(data)

      display.set_strip_config(data["configuration"])
          
      rtn["result"] = "Command sent!"
    except Exception as e: 
      print(e)
      rtn["result"] = None
      rtn["err"] = e
  else:
    try:      
      rtn["configuration"] = display.get_strip_config()    
    except Exception as e: 
      print(e)
      rtn["result"] = None
      rtn["err"] = e

  pprint.pprint(rtn)
  return jsonify(rtn)



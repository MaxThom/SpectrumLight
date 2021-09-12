
from flask import Blueprint, request, jsonify, render_template
import api.constants as constants
import api.utils as utils
import os.path
import subprocess
import pprint


animation_bp = Blueprint('animation', __name__)
q_command = None

def set_command_queue(p_q_command):
  global q_command
  q_command = p_q_command

@animation_bp.route('/')
def get():
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


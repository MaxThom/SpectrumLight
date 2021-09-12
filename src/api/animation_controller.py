
from flask import Blueprint, request, jsonify, render_template
import api.constants as constants
import api.utils as utils
import os.path
import subprocess
import pprint


animation_bp = Blueprint('animation', __name__)
q_command = None

@animation_bp.route('/')
def get():
  rtn = {}
  try:
    data = request.get_json()
    pprint.pprint(data)    

  except Exception as e: 
    print(e)
    rtn["result"] = None
    rtn["err"] = e

  pprint.pprint(rtn)
  return jsonify(rtn)


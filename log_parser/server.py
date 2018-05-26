import json
from . import handlers
from . import fields
from flask import Flask, request
from flask import jsonify
import flask
import sys
import traceback
from .config import config
from .config import abs_path

app = Flask(__name__)

EXTRA_KEY = "got an extra parameter"
MISSING_KEY = "missing parameter"
OK_REASON = "All OK"
RETURNED_NONE = "Handler returned None"
NO_PATH = "No such path exist"
EXCEPTION = "Handler has thrown an exception"
EXC_SERIALIZATION = "Serialization failed"
WRONG_METHOD = "No such method for this endpoint"

STATIC_FILES = [
  '/index.html',
  '/dist/build.js',
  '/static/pie-chart.svg'
]
ROOT = '/'

def placeholder_ep():
  pass

with open(abs_path(config['api_file']), 'r', encoding='utf-8') as f:
  content = json.loads(f.read())

for ep, value in content.items():
  app.route(ep, methods=value['methods'])(placeholder_ep)

def retcode(ok, reason, descr, data={}):
  try:
    return jsonify({
      fields.OK : ok,
      fields.REASON : reason,
      fields.DESCR : descr,
      fields.PAYLOAD : data
    })
  except:
    e = sys.exc_info()
    tr = traceback.TracebackException(*e)
    msg = list(tr.format())[-1].strip()
    return jsonify({
      fields.OK : False,
      fields.REASON : msg,
      fields.DESCR : EXC_SERIALIZATION,
      fields.PAYLOAD : {}
    })

def print_request(req):
  print("--- New request:", req.method, req.path)
  print("--- Params:", req.args.to_dict())

@app.before_request
def before_ep():
  global STATIC_FILES
  if request.path in STATIC_FILES:
    return flask.send_file(abs_path('web'+request.path))
  global ROOT
  if request.path == ROOT:
    return flask.send_file(abs_path('web'+STATIC_FILES[0]))
  global content
  print_request(request)
  if request.path not in content:
    return None # retcode(False, request.path, NO_PATH)
  if request.method not in content[request.path]['methods']:
    return retcode(False, request.method, WRONG_METHOD)
  request_params = request.args.to_dict(flat=False)
  for k in request_params:
    if k not in content[request.path]['params']:
      return retcode(False, k, EXTRA_KEY)
  for k in content[request.path]['params']:
    if k not in request_params:
      return retcode(False, k, MISSING_KEY)
  for k,v in request_params.items():
    if len(v) == 1:
      request_params[k] = v[0]
  # все параметры на месте
  if len(content[request.path]['methods']) > 1:
    request_params['method'] = request.method
  handler_name = 'handlers.'+content[request.path]['handler']+'_ep'
  try:
    ret = eval(handler_name)(**request_params)
  except:
    e = sys.exc_info()
    tr = traceback.TracebackException(*e)
    msg = list(tr.format())[-1].strip()
    return retcode(False, msg, EXCEPTION)
  if ret is None:
    return retcode(False, handler_name, RETURNED_NONE)
  if type(ret) == type((1,2,3)):
    ok, reason, data = ret
  else:
    ok, reason, data = True, None, ret
  if ok:
    return retcode(True, OK_REASON, OK_REASON, data=data)
  else:
    return retcode(False, reason, data)

@app.after_request
def apply_cors(response):
  response.headers['Access-Control-Allow-Origin'] = "*"
  return response

def start(ip, port):
  app.run(debug=False,threaded=False,processes=1,host=ip,port=port)

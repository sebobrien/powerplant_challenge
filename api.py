from flask import Flask, request, jsonify
from production_plan import *
app = Flask(__name__)


@app.route('/')
def hello():
    return "port 8888 baby!"

@app.route('/productionplan', methods=['POST'] )
def post():
    result = ""
    try:
        result = jsonify(generate_production_plan(request.get_json(force=True)))
    except RuntimeError as e:
        result = str(e)
    return result
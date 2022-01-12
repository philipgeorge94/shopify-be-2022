"""
Flask server to handle requests from frontend
Uses controller object
"""
import logging

from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin

import json
import webbrowser

from src.backend.controller.controller import Controller
from src.backend.model.model import Model
from src.backend.utils import map_utils

app = Flask(__name__, template_folder='../frontend/public')

# For Cross Origin Resource sharing
cors = CORS(app)

# Instantiate controller
ctr = Controller()

# Define all routes
@app.route('/', methods=['GET'])
@cross_origin()
def index():
    return render_template("index.html", token="Hello SEleNa")


@app.route('/route', methods=['POST'])
@cross_origin()
def route():

    # Get input and decode values
    data = json.loads(request.data)
    print(data)

    mode = data['mode']
    algo = data['algorithm']
    city = data['city']

    # Load specified graph
    map_file = "data/graph_" + city + ".pkl"
    graph = map_utils.load_map(map_file)

    limit = float(data['limit']) / 100

    model = Model()
    model.set_mode(mode)
    model.set_limit(limit)
    model.set_algorithm(algo)
    model.set_source(data['start'])
    model.set_destination(data['dest'])

    ctr.set_model(model)

    return ctr.handle_request(graph)


if __name__ == "__main__":
    logging.info("Starting Server")
    app.run()

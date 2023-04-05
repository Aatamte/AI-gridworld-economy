import os
from flask import Flask, Request, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import datetime
import numpy as np
from flask_cors import CORS, cross_origin
import threading
import subprocess
import logging
import time
import requests

# Initializing flask app
db = SQLAlchemy()
app = Flask(__name__)
CORS(app)
log = logging.getLogger('werkzeug')
log.disabled = True


DATA_STREAM = {
                "gridworld": [[0]],
                "agent_locations": [[0, 0]]
            }


@app.route('/data')
def update_gridworld():
    # Returning an api for showing in  reactjs
    return DATA_STREAM


@app.route('/frontend_ready', methods = ["POST"])
def get_status():
    status = request.json
    print(status)
    return status


class GridWorldReactServer:
    def __init__(
            self,
    ):
        self.app = app
        self.debug = False
        self.host: str = "127.0.0.1"

    def run(self):
        # start server on thread
        threading.Thread(
            target=lambda: app.run(
                port=5000,
                host=self.host,
                debug=self.debug,
                use_reloader=False
        )).start()

        cwd = os.getcwd()
        os.chdir(cwd + '/src/Visualization/frontend/gridworldeconomy')
        build = False
        if build:
            subprocess.Popen("serve -l 3000 -s build", shell=True)
        else:
            subprocess.Popen("npm run start", shell=True)

        os.chdir(cwd)
        time.sleep(10)

    def update(self, data):
        global DATA_STREAM
        DATA_STREAM = data
        update_gridworld()


# Running app
if __name__ == '__main__':
    app.run(debug=True)
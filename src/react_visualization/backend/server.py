import os
from flask import Flask, Request, Response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from src.utils import get_project_root, get_render_path
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
    return DATA_STREAM


class GridWorldReactServer:
    def __init__(
            self,
    ):
        self.app = app
        self.debug = False
        self.host: str = "127.0.0.1"
        self.port = 5000

    def run(self):
        # start server on thread
        threading.Thread(
            target=lambda: app.run(
                port=self.port,
                host=self.host,
                debug=self.debug,
                use_reloader=False
        )).start()

        cwd = os.getcwd()
        os.chdir(get_render_path())
        build = False
        if build:
            subprocess.Popen("serve -l 3000 -s build", shell=True)
        else:
            subprocess.Popen("npm run start", shell=True)
        os.chdir(cwd)
        time.sleep(2)

    @staticmethod
    def send(data):
        global DATA_STREAM
        temp_stream = {}
        for key in data.keys():
            if key not in DATA_STREAM.keys():
                temp_stream[key] = data[key]
            else:
                if data[key] != DATA_STREAM[key]:
                    temp_stream[key] = data[key]
        DATA_STREAM = temp_stream
        update_gridworld()


# Running app
if __name__ == '__main__':
    app.run(debug=True)
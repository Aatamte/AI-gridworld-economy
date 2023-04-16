import os
import sys
from pymongo import MongoClient
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
from multiprocessing import Process
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


class DatabaseServer:
    def __init__(self):
        self.debug = False
        self.host: str = "127.0.0.1"
        self.port = 5000
        self.server = threading.Thread(
            target=lambda: app.run(
                port=self.port,
                host=self.host,
                debug=self.debug,
                use_reloader=False
            )
        )

    def run(self):
        # start server on thread
        self.server.start()

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

    def close(self):
        print("shutting down")


client = MongoClient("mongodb://localhost:27017")


class MongoDBClient:
    def __init__(self):
        self.port = 5000
        self.mydb = client["mydatabase"]
        self.mycol = self.mydb["agents"]
        self.mycol.drop()

    def send(self):
        mylist = [
            {"_id": 1, "name": "John", "address": "Highway 37"},
            {"_id": 2, "name": "Peter", "address": "Lowstreet 27"},
            {"_id": 3, "name": "Amy", "address": "Apple st 652"},
            {"_id": 4, "name": "Hannah", "address": "Mountain 21"},
            {"_id": 5, "name": "Michael", "address": "Valley 345"},
            {"_id": 6, "name": "Sandy", "address": "Ocean blvd 2"},
            {"_id": 7, "name": "Betty", "address": "Green Grass 1"},
            {"_id": 8, "name": "Richard", "address": "Sky st 331"},
            {"_id": 9, "name": "Susan", "address": "One way 98"},
            {"_id": 10, "name": "Vicky", "address": "Yellow Garden 2"},
            {"_id": 11, "name": "Ben", "address": "Park Lane 38"},
            {"_id": 12, "name": "William", "address": "Central st 954"},
            {"_id": 13, "name": "Chuck", "address": "Main Road 989"},
            {"_id": 14, "name": "Viola", "address": "Sideway 1633"}
        ]

        x = self.mycol.insert_many(mylist)


# Running app
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import threading
import logging

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

# Running app
if __name__ == '__main__':
    app.run(debug=True)
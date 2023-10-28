import logging

from flask import Flask, render_template
from flask_cors import CORS

from app import settings
from app.config.db import db
from app.socket.websocket import socketio

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("./logs/app.log"),
        logging.StreamHandler(),
    ],
    format="%(asctime)s - [%(levelname)8s] %(process)d %(name)20s : %(message)s",
)

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = settings.MONGODB_SETTINGS
logger = logging.getLogger()

db.init_app(app)
socketio.init_app(app)
CORS(app)


@app.errorhandler(404)
def page_not_found(_):
    return render_template("404.html"), 404


if __name__ == "__main__":
    socketio.run(app, debug=settings.DEBUG, host="0.0.0.0", port=settings.PORT)

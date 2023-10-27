import sys
import json
import logging

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from app.utils.db import db
from app import settings

logging.basicConfig(
    filename='./logs/app.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = settings.MONGODB_SETTINGS
socketio = SocketIO(app, cors_allowed_origins='*')
logger = logging.getLogger()

db.init_app(app)

@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.html'), 404


if __name__ == "__main__":
    socketio.run(app, debug=settings.DEBUG)

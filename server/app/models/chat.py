import datetime

from flask_mongoengine import Document

from app.config.db import db


class Chats(Document):
    email = db.StringField(max_length=0xFF, required=True)
    prompt = db.StringField(max_length=0xFF, required=True)
    reply = db.StringField(max_length=0xFF, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)

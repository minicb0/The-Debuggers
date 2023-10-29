import logging

from flask import Blueprint, request
from flask_cors import CORS

from app.models.chat import Chats

feedback = Blueprint("feedback", __name__, url_prefix="/feedback")
logger = logging.getLogger(__name__)

CORS(feedback)


@feedback.route("/", methods=["POST"])
def submit_feedback():
    data = request.json

    chat_id = data.get("chat_id")
    fb = data.get("feedback")

    fb = fb.lower()

    if fb not in ("positive", "negetive", "neutral"):
        return "Not a proper feedback", 400

    chat = Chats.objects(pk=chat_id).first()

    if chat is None:
        return "Invalid id", 400

    chat.feedback = fb
    chat.save()
    logger.info(f"{fb} feedback registered for chat-id: {chat_id}")
    return "Feedback saved successfully", 200

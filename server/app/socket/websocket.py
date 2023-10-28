import logging

from flask import request
from flask_socketio import Namespace, SocketIO

from app.models.chat import Chats

# from app.nlp_engine.response import get_response
from app.utils.speech_to_text import speech_to_text, translateMessage

socketio = SocketIO(cors_allowed_origins="*", logger=True)


class ChatClient(Namespace):
    _logger = logging.getLogger(__name__)

    def on_connect(self):
        self.client_id = request.sid
        self._logger.info(f"{self} connected")

    def on_disconnect(self):
        self._logger.info(f"{self} disconnected")

    def on_email(self, email):
        self.email = email

    def on_message(self, message: str):
        self._logger.info(f"{self} sent message: {message}")
        english, src = translateMessage(message)
        self._logger.info(f"language detected: {src}")
        # results = get_response(english)
        # self._logger.info(f"response of {message}: {results}")
        # response, _ = translateMessage(results, to=src)

        self.emit("response", english, room=self.client_id)

        chat = Chats(email=self.email, prompt=message, reply=english)

        chat.save()

    def on_voice(self, data: str):
        self._logger.info(f"{self} sent voice message")
        data = data.split(",")[1]
        message = speech_to_text(data)
        english, src = translateMessage(message)
        response, _ = translateMessage(english, to=src)

        self.emit("response", response, room=self.client_id)

        chat = Chats(email=self.email, prompt=message, reply=response)

        chat.save()


socketio.on_namespace(ChatClient("/chat"))

import json
import logging

from flask import request
from flask_socketio import Namespace, SocketIO

from app.models.chat import Chats
from app.nlp_engine.response import get_response

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
        self._logger.info(f"{self} connected with email: {email}")
        self.email = email

    def on_message(self, message: str):
        self._logger.info(f"{self} sent message: {message}")
        # english, src = translateMessage(message)
        # self._logger.info(f"language detected: {src}")
        results = get_response(message)
        # self._logger.info(f"response of {message}: {results}")
        # response, _ = translateMessage(results, to=src)
        chat = Chats(
            email=self.email, prompt=message, reply=results, feedback="neutral"
        )
        chat.save()
        self._logger.info(str(chat.pk))
        self.emit("response", json.dumps({"id": str(chat.pk), "data": results}))

    def on_voice(self, data: str):
        self._logger.info(f"{self} sent voice message")
        data = data.split(",")[1]
        message = speech_to_text(data)
        english, src = translateMessage(message)
        results = get_response(english)
        response, _ = translateMessage(results, to=src)
        chat = Chats(
            email=self.email, prompt=message, reply=response, feedback="neutral"
        )
        chat.save()
        self.emit("response", json.dumps({"id": str(chat.pk), "data": response}))
        self._logger.info(
            f"{self} src: {src}, message: {message}, english: {english}, results: {results}, response: {response}"
        )


socketio.on_namespace(ChatClient("/chat"))

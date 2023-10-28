import logging

from flask_socketio import Namespace, SocketIO

from app.utils.speech_to_text import speech_to_text, translateMessage

socketio = SocketIO(cors_allowed_origins="*", logger=True)


class ChatClient(Namespace):
    _logger = logging.getLogger(__name__)

    def on_connect(self):
        self._logger.info(f"{self} connected")

    def on_disconnect(self):
        self._logger.info(f"{self} disconnected")

    def on_message(self, message: str):
        self._logger.info(f"{self} sent message: {message}")
        english, src = translateMessage(message)
        response, _ = translateMessage(english, to=src)
        self.emit("response", response)

    def on_voice(self, data: str):
        self._logger.info(f"{self} sent voice message")
        message = speech_to_text(data)
        english, src = translateMessage(message)
        response, _ = translateMessage(english, to=src)
        self.emit("response", response)


socketio.on_namespace(ChatClient("/chat"))

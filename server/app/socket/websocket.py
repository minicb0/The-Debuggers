import logging
from flask_socketio import Namespace, SocketIO
from app.nlp_engine.response import get_response

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
        self._logger.info(f"language detected: {src}")
        results = get_response(english)
        self._logger.info(f"response of {message}: {results}")
        response, _ = translateMessage(results, to=src)
        
        self.emit("response", response)

    def on_voice(self, data: str):
        self._logger.info(f"{self} sent voice message")
        data = data[22:]
        print(data, len(data))
        message = speech_to_text(data)
        english, src = translateMessage(message)
        response, _ = translateMessage(english, to=src)
        self.emit("response", response)
        self.logger.info(f"{self} disconnected")


socketio.on_namespace(ChatClient("/chat"))

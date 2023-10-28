import logging

from flask_socketio import Namespace, SocketIO

socketio = SocketIO(cors_allowed_origins="*", logger=True)


class ChatClient(Namespace):
    logger = logging.getLogger(__name__)

    def on_connect(self):
        self.logger.info(f"{self} connected")

    def on_disconnect(self):
        self.logger.info(f"{self} disconnected")

    def on_message(self, message):
        self.logger.info(f"{self} sent message: {message}")
        self.emit("response", f"Received: {message[::-1]}")


socketio.on_namespace(ChatClient("/chat"))

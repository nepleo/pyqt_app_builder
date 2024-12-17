from enum import Enum
from typing import Dict, Callable, Any


class MessageType(Enum):
    LOGIN = "Login"
    # 其他消息类型...


class MessageHandler:
    def __init__(self):
        self._handlers: Dict[MessageType, Callable] = {}

    def register_handler(self, msg_type: MessageType, handler: Callable):
        self._handlers[msg_type] = handler

    def handle_message(self, data: Dict[str, Any]) -> Any:
        msg_type = data.get("type")
        try:
            msg_type_enum = MessageType(msg_type)
            handler = self._handlers.get(msg_type_enum)
            if handler:
                return handler(data)
        except ValueError:
            print(f"Unknown message type: {msg_type}")
        return None

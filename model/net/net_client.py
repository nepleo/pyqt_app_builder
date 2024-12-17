from typing import Callable, Optional
from model.utils.utils import json_to_dict
from model.net.socket import SocketClient
from model.net.crc32 import create_message, parse_message


class NetClient:
    """接收str类型的字符串,组包|解包后发出"""

    def __init__(self, host, port):
        self.socket_client = SocketClient(host=host, port=port)
        self._callback: Optional[Callable] = None

    def connect(self) -> bool:
        return self.socket_client.connect()

    def disconnect(self):
        self.socket_client.disconnect()

    def is_connected(self) -> bool:
        return self.socket_client.is_connected()

    def register_callback(self, callback):
        def wrapped_callback(data: str):
            # 1. 解析网络协议
            parsed_data = parse_message(data)
            # 2. 解析JSON数据
            msg_dict = json_to_dict(parsed_data)
            # 3. 调用实际的回调
            callback(msg_dict)

        self._callback = wrapped_callback
        self.socket_client.register_callback(self._callback)

    def send(self, data: str) -> bool:
        # 添加网络协议包装
        wrapped_msg = create_message(data)
        return self.socket_client.send_data(wrapped_msg)

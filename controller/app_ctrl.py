# coding=utf-8
from controller.login_ctrl import LoginController
from model.message.msg_handler import MessageHandler, MessageType
from model.net.net_client import NetClient
from model.config import Config
from view.login_window import LoginWindow
from view.window_mgr import WindowManager
from typing import Dict, Any


class AppController:
    def __init__(self) -> None:
        self._window_mgr = WindowManager()
        self._network_client = None
        self._config = None
        self._message_handler = None
        self._login_ctrl = None
        self._setup()

    def _setup(self):
        self._init_config()
        self._init_network_client()
        self._init_windows()
        self._init_controllers()
        self._init_message_handler()

    def _init_config(self):
        self._config = Config()

    def _init_windows(self):
        self._window_mgr.register_window("login", LoginWindow())

    def _init_network_client(self):
        self._network_client = NetClient(
            self._config.get("host"), int(self._config.get("port"))
        )
        self._network_client.register_callback(self._on_message_received)
        self._network_client.connect()

    def _init_controllers(self):
        self._login_ctrl = LoginController(self._window_mgr, self._network_client)

    def _init_message_handler(self):
        self._message_handler = MessageHandler()
        self._message_handler.register_handler(
            MessageType.LOGIN, self._login_ctrl.handle_login_response
        )
        self._network_client.register_callback(self._on_message_received)

    def start(self):
        login_window = self._window_mgr.get_window("login")
        login_window.show()

    def stop(self):
        if self._network_client:
            self._network_client.disconnect()

    def _on_message_received(self, data: Dict[str, Any]):
        if data:
            self._message_handler.handle_message(data)

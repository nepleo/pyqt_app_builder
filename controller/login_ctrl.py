from model.protocols.login_protocol import LoginProtocol
from model.net.net_client import NetClient
from view.window_mgr import WindowManager


class LoginController:
    def __init__(self, window_mgr: WindowManager, net_client: NetClient):
        self._window_mgr = window_mgr
        self._net_client = net_client
        self._protocol = LoginProtocol()
        self._login_window = window_mgr.get_window("login")
        self._init_signals()

    def _init_signals(self):
        self._login_window.signal_btn_login_clicked.connect(self._on_login)

    def _on_login(self, username: str, password: str):
        msg = self._protocol.serialize(username=username, password=password)
        self._net_client.send(msg)

    def handle_login_response(self, data: str):
        result = self._protocol.deserialize(data)
        if result["status"] == "success":
            pass
            # self._window_mgr.switch_window("login", "main")
        else:
            self._login_window.show_login_failed()

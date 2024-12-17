from typing import Dict
from PyQt5.QtWidgets import QWidget


# 窗口切换,窗口隐藏,窗口注册
class WindowManager:
    def __init__(self):
        self._windows: Dict[str, QWidget] = {}
        self._current_window = None

    def register_window(self, name: str, window: QWidget):
        self._windows[name] = window

    def get_window(self, name):
        return self._windows.get(name)

    def show_window(self, name):
        if window := self.get_window(name):
            window.show()

    def hide_window(self, name):
        if window := self.get_window(name):
            window.show()

    def switch_window(self, from_name, to_name):
        self.hide_window(from_name)
        self.show_window(to_name)

import sys
import typing

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QPixmap, QCloseEvent
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import MessageBox, isDarkTheme
from .gen.Ui_LoginWindow import Ui_LoginWindow
from model.utils import is_win11

if is_win11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class LoginWindow(Window):
    # view层对外暴露的信号
    signal_btn_login_clicked = pyqtSignal(str, str)
    signal_about_to_close = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self._init_window()
        self._init_signals()

    def _init_window(self):
        self.resize(400, 260)
        self.setWindowIcon(QIcon(QPixmap(":/images/logo.png")))
        self.setWindowTitle("Login")
        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=isDarkTheme())
        self._center_window()

    def _center_window(self):
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def _init_signals(self):
        self.ui.ldt_passwd.returnPressed.connect(self._on_login_clicked)
        self.ui.btn_login.clicked.connect(self._on_login_clicked)

    def _on_login_clicked(self):
        username = self.ui.ldt_username.text()
        passwd = self.ui.ldt_passwd.text()
        self.signal_btn_login_clicked.emit(username, passwd)

    def _show_error_msg(self, title: str, message: str):
        msg_box = MessageBox(title, message, self)
        msg_box.cancelButton.hide()
        msg_box.yesButton.setText("OK")
        msg_box.exec()

    def _clear_inputs(self):
        self.ui.ldt_username.clear()
        self.ui.ldt_passwd.clear()

    def show_login_failed(self):
        self._show_error_msg("WARN", "LOGIN FAILED")
        self.ui.ldt_passwd.clear()
        self.ui.ldt_passwd.setFocus()

    def show_connect_refused(self):
        self._show_error_msg("WARN", "SERVER CONNECT REFUSED")

    def show_window_title(self, msg: str):
        self.lbl_title.setText(str)

    def closeEvent(self, event: typing.Optional[QCloseEvent]) -> None:
        self.signal_about_to_close.emit()


if __name__ == "__main__":

    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    sys.exit(app.exec_())

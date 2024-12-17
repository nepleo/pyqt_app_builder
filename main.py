import sys
import os
import glob
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication
from qframelesswindow.utils import getSystemAccentColor
from qfluentwidgets import setThemeColor

from controller.app_ctrl import AppController
from model.process import TradeBackend
from model.utils.log import setup_logging
from resource.gen import resource_rc

# 设置logger
setup_logging()


def init_app():
    """初始化QApplication"""
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # 设置全局字体和主题
    font = QFont("Segoe UI")
    app.setFont(font)
    setThemeColor(getSystemAccentColor(), save=False)
    app.setWindowIcon(QIcon(":/icons/logo.ico"))

    return app


def find_trader_exe():
    """
    查找交易后端程序
    """
    script_path = os.path.dirname(sys.executable)
    trader_path = os.path.join(script_path, "trade.exe")
    return trader_path


def main():
    # 1. 初始化QApplication
    app = init_app()

    # 2. 启动后端进程
    trader_path = find_trader_exe()
    trader = TradeBackend(trader_path)
    if not trader.start_backend():
        print("Failed to start backend process")
        # return

    try:
        # 3. 启动主程序
        controller = AppController()
        controller.start()

        # 4. 运行事件循环
        result = app.exec_()

    finally:
        # 5. 清理资源
        controller.stop()
        trader.stop_backend()
        sys.exit(result)


if __name__ == "__main__":
    main()

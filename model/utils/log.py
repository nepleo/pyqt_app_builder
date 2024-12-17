import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    """
    设置日志
    - 创建日志目录
    - 配置日志格式
    - 设置日志级别
    """
    # 确保日志目录存在
    log_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "log"
    )
    os.makedirs(log_dir, exist_ok=True)

    log_filename = os.path.join(log_dir, "app.log")

    # 配置日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # 文件处理器 (with rotation)
    file_handler = RotatingFileHandler(
        log_filename, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"  # 10MB
    )
    file_handler.setFormatter(formatter)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # 记录启动日志
    logging.info("Logging system initialized")

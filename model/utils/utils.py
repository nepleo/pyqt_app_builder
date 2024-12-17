import sys
import json
from typing import Dict, Any
from PyQt5.QtCore import QFile, QTextStream, QResource


def is_win11():
    return sys.platform == "win32" and sys.getwindowsversion().build >= 22000


# 加载 QSS 文件
def load_qss_from_resource(resource_name):
    qss_file = QFile(":/styles/" + resource_name)
    if not qss_file.open(QFile.ReadOnly | QFile.Text):
        print(f"Failed to load QSS resource: {resource_name}")
        return ""
    stream = QTextStream(qss_file)
    return stream.readAll()


def dict_to_json(data: Dict[str, Any]) -> str:
    """
    将字典转换为JSON字符串
    Args:
        data: 要转换的字典
    Returns:
        str: JSON字符串
    """
    try:
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        print(f"Failed to convert dict to JSON: {e}")
        return ""


def json_to_dict(json_str: str) -> Dict[str, Any]:
    """
    将JSON字符串转换为字典
    Args:
        json_str: JSON字符串
    Returns:
        Dict: 转换后的字典，如果转换失败返回空字典
    """
    try:
        return json.loads(json_str)
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        return {}

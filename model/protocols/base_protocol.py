from abc import ABC, abstractmethod
from typing import Dict, Any
from model.utils.utils import dict_to_json, json_to_dict


class BaseProtocol(ABC):
    @abstractmethod
    def _build_message(self, **kwargs) -> Dict[str, Any]:
        """构建消息字典"""
        pass

    @abstractmethod
    def _parse_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """解析消息字典"""
        pass

    def serialize(self, **kwargs) -> str:
        """
        将参数序列化为JSON字符串
        Returns:
            str: JSON字符串
        """
        msg_dict = self._build_message(**kwargs)
        return dict_to_json(msg_dict)

    def deserialize(self, data: str) -> Dict[str, Any]:
        """
        将JSON字符串反序列化为参数字典
        Args:
            data: JSON字符串
        Returns:
            Dict: 参数字典
        """
        msg_dict = json_to_dict(data)
        return self._parse_message(msg_dict)

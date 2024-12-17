from typing import Dict, Any
from .base_protocol import BaseProtocol


class LoginProtocol(BaseProtocol):
    def _build_message(self, username: str, password: str) -> Dict[str, Any]:
        return {
            "type": "Login",
            "data": {
                "username": username,
                "password": password
            }
        }
    
    def _parse_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": data.get("status"),
            "uid": data.get("data", {}).get("uid")
        } 
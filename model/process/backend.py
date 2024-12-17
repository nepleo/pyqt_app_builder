import os
import subprocess
from typing import Optional


class TradeBackend:
    def __init__(self, exe_path: str):
        self.exe_path = exe_path
        self._process: Optional[subprocess.Popen] = None

    def start_backend(self) -> bool:
        if not os.path.exists(self.exe_path):
            print(f"Backend executable not found: {self.exe_path}")
            return False

        try:
            self._process = subprocess.Popen(
                [self.exe_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            return True
        except Exception as e:
            print(f"Failed to start backend: {e}")
            return False

    def stop_backend(self):
        if self._process:
            self._process.terminate()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()
            self._process = None

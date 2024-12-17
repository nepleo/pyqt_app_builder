import socket
import struct
import threading
import time
from typing import Optional
from pydispatch import dispatcher


class SocketClient:
    HEADER_SIZE = 4
    RECONNECT_INTERVAL = 5  # seconds
    MAX_RECONNECT_ATTEMPTS = 3

    def __init__(self, host, port, timeout=100):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket: Optional[socket.socket] = None
        self.receive_thread = None
        self.callback = None
        self.receive_thread_running = False
        self.connected = False
        self.reconnect_attempts = 0

    def __del__(self):
        self.disconnect()

    def connect(self) -> bool:
        if self.is_connected():
            return True

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.receive_thread_running = True
            self.receive_thread = threading.Thread(target=self._receive_data_thread)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            self.reconnect_attempts = 0
            return True

        except (ConnectionRefusedError, socket.timeout) as e:
            print(f"Connection failed: {str(e)}")
            self._handle_connection_error()
            return False

    def _handle_connection_error(self):
        self.connected = False
        if self._reconnect_attempts < self.MAX_RECONNECT_ATTEMPTS:
            self._reconnect_attempts += 1
            print(
                f"Attempting to reconnect ({self._reconnect_attempts}/{self.MAX_RECONNECT_ATTEMPTS})..."
            )
            time.sleep(self.RECONNECT_INTERVAL)
            self.connect()
        else:
            print("Max reconnection attempts reached")
            dispatcher.send(signal="connection_error")

    def disconnect(self):
        if self.socket is not None and self.socket.fileno() != -1:
            self.socket.close()
        self.receive_thread_running = False
        self.connected = False
        if self.receive_thread is not None:
            self.receive_thread.join()

    def is_connected(self) -> bool:
        return self.connected and self.socket is not None

    # 发送的数据类型是bytes
    def send_data(self, data) -> bool:
        if not self.is_connected():
            return False

        try:
            self.socket.sendall(data)
            return True
        except Exception as e:
            print("Error sending data:", str(e))
            self._handle_connection_error()
            return False

    def _receive_data_thread(self):
        while self.receive_thread_running and self.is_connected():
            try:
                # 1. 首先读取4字节的消息头(消息长度)
                header_data = self._recv_all(self.HEADER_SIZE)
                if not header_data:
                    break

                # 2. 解析消息总长度
                total_length = struct.unpack("!I", header_data)[0]

                # 3. 读取剩余的消息内容(实际消息 + CRC 长度)(不是特别规范 按道理来说是整个包的长度)
                message_data = self._recv_all(total_length)
                if not message_data:
                    break

                # 4. 组合完整消息
                complete_message = header_data + message_data

                # 5. 调用回调处理消息
                if self.callback:
                    self.callback(complete_message)

            except TimeoutError as e:
                continue
            except ConnectionError as e:
                print("Error receiving data:", str(e))
                self._handle_connection_error()
                break
            except Exception as e:
                print("Error receiving data:", str(e))
                self._handle_connection_error()
                break

    def register_callback(self, callback):
        self.callback = callback

    def _recv_all(self, size):
        """确保接收指定大小的数据"""
        data = bytearray()
        while len(data) < size:
            try:
                packet = self.socket.recv(size - len(data))
                if not packet:
                    return None
                data.extend(packet)
            except socket.timeout:
                continue
        return data

import struct

POLYNOMIAL = 0xEDB88320

CRC32_TABLE = [0] * 256

HEADER_SIZE = 4
CRC_SIZE = 4
MIN_DATA_SIZE = HEADER_SIZE + CRC_SIZE


def generate_table():
    for i in range(256):
        crc = i
        for j in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ POLYNOMIAL
            else:
                crc >>= 1
        CRC32_TABLE[i] = crc


def compute_crc32(data: bytes) -> int:
    if CRC32_TABLE[1] == 0:
        generate_table()

    crc_value = 0xFFFFFFFF
    for byte in data:
        table_index = byte ^ (crc_value & 0xFF)
        crc_value = CRC32_TABLE[table_index] ^ (crc_value >> 8)
    return crc_value ^ 0xFFFFFFFF


def parse_message(data: bytes) -> str:
    if len(data) < MIN_DATA_SIZE:
        return ""

    data_length = struct.unpack("!I", data[:HEADER_SIZE])[0]
    if (data_length + HEADER_SIZE) != len(data):
        return ""

    message_length = data_length - 4
    received = data[HEADER_SIZE : HEADER_SIZE + message_length]
    recv_crc_value = struct.unpack(
        "!I",
        data[HEADER_SIZE + message_length : HEADER_SIZE + message_length + CRC_SIZE],
    )[0]
    cal_crc_value = compute_crc32(received)
    if recv_crc_value != cal_crc_value:
        return ""

    return received.decode()


def create_message(content: str) -> bytes:
    message_length = len(content)
    data_length = struct.pack("!I", message_length + CRC_SIZE)
    crc_value = struct.pack("!I", compute_crc32(content.encode()))
    message = data_length + content.encode() + crc_value
    return message


# 示例用法
if __name__ == "__main__":
    # CRC32 计算示例
    data_example = "Hello, world!"
    crc32_value = compute_crc32(data_example.encode())
    print("CRC32 value:", crc32_value)

    # 消息解析和创建示例
    content_example = "Hello, world!"
    message_example = create_message(content_example)
    print("Created message:", message_example)

    parsed_content = parse_message(message_example)
    print("Parsed content:", parsed_content)

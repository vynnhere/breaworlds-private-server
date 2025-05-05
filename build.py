import io

@staticmethod
def write_int(value: int, hex_length: int, buffer: io.BytesIO):
    bytes_list = []
    for i in range(hex_length):
        byte = (value >> (8 * i)) & 0xFF
        bytes_list.append(byte)
    buffer.write(bytes(bytes_list))
    
@staticmethod
def write_string(s: str, buffer: io.BytesIO, is_null=True):
    encoded = s.encode('utf-8')
    if is_null:
        encoded += b'\x00'
    buffer.write(encoded)
    
@staticmethod
def writer(value: int, buffer: io.BytesIO):
    # dummy 0000
    buffer.write(b'\x00\x00')
    
    low = value & 0xFF
    high = (value >> 8) & 0xFF
    buffer.write(bytes([low, high]))
    
@staticmethod
def create_packet(buffer: io.BytesIO):
    buffer.seek(0)
    length = buffer.getbuffer().nbytes
        
    low = length & 0xFF
    high = (length >> 8) & 0xFF
    buffer.write(bytes([low, high]))
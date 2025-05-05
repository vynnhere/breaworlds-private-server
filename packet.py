from server import *
import build, io, struct

class encode:
    def log(text: str, client: socket.socket):
        buffer = io.BytesIO()
        build.writer(4, buffer)
        build.write_string(text, buffer)
        build.create_packet(buffer)
          
        send_data(client, buffer.getvalue())
        buffer.close()
    
    class world:
        def world_load(client: socket.socket):
            buffer = io.BytesIO()
            buffer.write(struct.pack("<H", 0))
            buffer.write(struct.pack("<H", 10))
            
            buffer.write(struct.pack("<H", 100))
            buffer.write(struct.pack("<H", 50))
            
            for x in range(100):
                for y in range(50):
                    buffer.write(struct.pack("<H", 0))
                    buffer.write(struct.pack("<H", 9 if y >= 25 else 0))
                    buffer.write(struct.pack("<H", 0))
                    buffer.write(struct.pack("<H", 0))
            
            buffer.seek(0)
            buffer.write(struct.pack("<H", buffer.getbuffer().nbytes))
            
            send_data(client, buffer.getvalue())
            buffer.close()
        
        def update_tile(x: int, y: int, layer: int, id: int, client: socket.socket):
            buffer = io.BytesIO()
            buffer.write(struct.pack("<H", 0))
            buffer.write(struct.pack("<H", 11))
            buffer.write(struct.pack("<H", x))
            buffer.write(struct.pack("<H", y))
            buffer.write(struct.pack("<H", layer))
            buffer.write(struct.pack("<H", id))

            buffer.seek(0)
            buffer.write(struct.pack("<H", buffer.getbuffer().nbytes))

            # return buffer.getvalue()
            send_data(client, buffer.getvalue())
            buffer.close()

        def world_result(success: bool, message: str, worldname: str, client: socket.socket):
            buffer = io.BytesIO()
            build.writer(8, buffer)
            build.write_int(int(success), 2, buffer)
            build.write_string(message, buffer)
            build.write_string(worldname, buffer)
            build.create_packet(buffer)

            send_data(client, buffer.getvalue())
            buffer.close()
            

        def update_gems(amount: int, goods: bool, client: socket.socket):        
            buffer = io.BytesIO()
            build.writer(16, buffer)
            build.write_int(amount, 14, buffer)
            build.write_int(int(goods), 2, buffer)
            build.create_packet(buffer)

            send_data(client, buffer.getvalue())
            buffer.close()

        def update_position(identifier: int, x: int, y: int, new_player: bool, client: socket.socket):
            buffer = io.BytesIO()
            buffer.write(struct.pack('<H', 0))
            buffer.write(struct.pack('<H', 13))
            buffer.write(struct.pack('i', identifier))
            buffer.write(struct.pack('?', new_player))
            buffer.write(struct.pack('<H', x))
            buffer.write(struct.pack('<H', y))
            buffer.seek(0)
            buffer.write(struct.pack('H', buffer.getbuffer().nbytes))

            send_data(client, buffer.getvalue())
            buffer.close()
        
        def update_character(identifier, skin_color_red: int, skin_color_green: int, skin_color_blue: int, skin_alpha: int, sex: int, badge: int, jump: int, username: str, visible: bool, noclip: bool, frozen: bool, jump_height: int, walk_speed: int, client: socket.socket):
            pkt = io.BytesIO()
            build.writer(14, pkt)
            build.write_int(identifier, 4, pkt)
            build.write_int(skin_color_red, 2, pkt)
            build.write_int(skin_color_green, 2, pkt)
            build.write_int(skin_color_blue, 2, pkt)
            build.write_int(skin_alpha, 2, pkt)
            build.write_int(sex, 1, pkt)
            build.write_int(badge, 2, pkt)
            build.write_int(jump, 2, pkt)
            build.write_string(username, pkt)
            
            for i in range(21):
                build.write_int(0, 2, pkt)

            build.write_int(100, 2, pkt)
            build.write_int(0, 1, pkt)
            build.write_int(0, 1, pkt)
            build.write_int(int(visible), 1, pkt)
            build.write_int(int(noclip), 1, pkt)
            build.write_int(int(frozen), 1, pkt)
            build.write_int(int(False), 1, pkt)
            build.write_int(jump_height, 2, pkt)
            build.write_int(walk_speed, 2, pkt)

            build.write_int(0, 3, pkt)
            build.write_int(0, 2, pkt)
            build.write_int(0, 2, pkt)
            build.write_int(0, 2, pkt)

            build.create_packet(pkt)

            send_data(client, pkt.getvalue())
            pkt.close()

        def update_inventory(items, client: socket.socket):
            buffer = io.BytesIO()
            build.writer(6, buffer)
            for item in items:
                build.write_int(item["id"], 2, buffer)
                build.write_int(item["quantity"], 2, buffer)
                build.write_int(item["icon"], 2, buffer)
            build.create_packet(buffer)

            send_data(client, buffer.getvalue())
            buffer.close()

class decode:
    def extract_place(dada: bytes) -> bytes:
        buffer = io.BytesIO(dada)
        a = struct.unpack('<H', buffer.read(2))[0]
        b = struct.unpack('<H', buffer.read(2))[0]

        x = struct.unpack('<H', buffer.read(2))[0] // 32
        y = struct.unpack('<H', buffer.read(2))[0] // 32
        id = struct.unpack('<H', buffer.read(2))[0]

        c = struct.unpack('<H', buffer.read(2))[0]

        return x, y, id
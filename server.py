# Written by @vynnhere a.k.a breajesus
# Credits to @aqeel a.k.a adamwibu
# This is a historical early build of CreativeBW.

import socket, threading, select, sys, packet, io, time

server_ip = "0.0.0.0"
server_port = 1800

def server_loop():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((server_ip, server_port))
        server.listen(5)
        print(f"Server listening on {server_ip}:{server_port}")
    except Exception as e:
        print(f"failed to bind server: {e}")
        sys.exit(1)
    
    while True:
        try:
            client, address = server.accept()
            print(f"Connection from {address[0]}:{address[1]}")
            handler_thread = threading.Thread(target=server_handler, args=(client,))
            handler_thread.start()
        except Exception as e:
            print(f"failed to accept connection: {e}")

def server_handler(player: socket.socket):
    try:
        player.setblocking(0)

        while True:
            if (client_data := receive_data(player)):
                if client_data is None:
                    break

                try:
                    buf = io.BytesIO(client_data)
                    buf.read(2)
                    pkt_type = buf.read(1)
                    
                    match pkt_type:
                        case b'\x00':
                            if b"\r4.0.0.2.8.5.3" in client_data:
                                packet.encode.log("Basic Breaworlds Private Server", player)
                        
                        case b'\x01':
                            packet.encode.world.update_gems(100, False, player)

                            packet.encode.world.update_inventory([{'id': 1, 'quantity': 1, 'icon': 1}, {'id': 9, 'quantity': 500, 'icon': 1}, {'id': 11, 'quantity': 500, 'icon': 1}, {'id': 13, 'quantity': 500, 'icon': 1}, {'id': 15, 'quantity': 500, 'icon': 1}, {'id': 17, 'quantity': 500, 'icon': 1}, {'id': 19, 'quantity': 500, 'icon': 1}, {'id': 21, 'quantity': 500, 'icon': 1}, {'id': 23, 'quantity': 500, 'icon': 1}, {'id': 25, 'quantity': 500, 'icon': 1}, {'id': 27, 'quantity': 500, 'icon': 1}, {'id': 29, 'quantity': 500, 'icon': 1}, {'id': 31, 'quantity': 500, 'icon': 1}, {'id': 33, 'quantity': 500, 'icon': 1}, {'id': 35, 'quantity': 500, 'icon': 1}, {'id': 37, 'quantity': 500, 'icon': 1}, {'id': 39, 'quantity': 500, 'icon': 1}, {'id': 41, 'quantity': 500, 'icon': 1}, {'id': 43, 'quantity': 500, 'icon': 1}, {'id': 45, 'quantity': 500, 'icon': 1}, {'id': 47, 'quantity': 500, 'icon': 1}, {'id': 49, 'quantity': 500, 'icon': 1}, {'id': 51, 'quantity': 500, 'icon': 1}], player)

                            packet.encode.world.world_result(True, "~0Loaded...", "WORLD", player)

                            time.sleep(2)

                            packet.encode.world.world_load(player)
                                
                            packet.encode.world.update_position(0, 0, 768, False, player)
                            
                            packet.encode.world.update_character(0, 255, 255, 255, 100, 0, 0, 0, "Player", True, True, False, 15, 1, player)
                        
                        case b'\x0b':
                            x, y, id = packet.decode.extract_place(client_data)

                            if id == 1: id = 0

                            packet.encode.world.update_tile(x, y, 2, id, player)

                except:
                    pass    

    except Exception as e:
        print(f"eror in handler: {e}")

def send_data(player: socket.socket, data: bytes):
    try:
        player.sendall(data)
    except Exception as e:
        print(f"eror send: {e}")

        player.close()
        player = None
        sys.exit(1)

def receive_data(player: socket.socket) -> bytes:
    try:
        ready = select.select([player], [], [], 0.1)
        if ready[0]:
            data = player.recv(4096)
            if data: return data

    except Exception as e:
        print(f"eror receive: {e}")
    
        player.close()
        player = None
        sys.exit(1)
        
    return None

if __name__ == "__main__":
    print("Starting server...")
    server_thread = threading.Thread(target=server_loop)
    server_thread.start()
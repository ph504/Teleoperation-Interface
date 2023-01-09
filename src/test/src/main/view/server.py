import socket 
import socketserver

HOST = '192.168.2.15'
PORT = 4001

socketserver.TCPServer.allow_reuse_address = True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            data = data.decode('utf-8')
            if not data:
                break
            
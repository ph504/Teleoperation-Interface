import socket 


HOST = '192.168.2.15'
PORT = 4001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)
while True:
    conn, addr = s.accept()
    data = conn.recv(1024)
    data = data.decode('utf-8')
    print("Message from: " + str(addr))
    print("From connected user: " + data)
    conn.close()
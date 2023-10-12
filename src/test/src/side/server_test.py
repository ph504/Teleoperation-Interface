import socket
import socketserver
    
socketserver.TCPServer.allow_reuse_address = True

HOST = '192.168.2.191'
PORT = 4001

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()
            s.settimeout(None)
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                break
                while True:
                    try:
                        data = conn.recv(1024)
                        data = data.decode('utf-8')
                        if not data:
                            break
                        ack = "ACK"
                        conn.send(ack.encode('utf-8'))
                    except socket.timeout:
                            print("timeout error!!!!")
                            break
                
                    print("From connected user: " + data)
                    if int(data) == 0:
                        Logger.log("calibration", 1)
                        EventManager.post_event("activate_calibration", -1)
                    else:
                        Logger.log("collision", data)
                        EventManager.post_event("collision", data)
        
        except Exception as e:
            print("shit happened: " + str(e))  
            break      

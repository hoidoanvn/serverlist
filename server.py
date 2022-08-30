"""
Khởi tạo một process
trong process này có thể khởi tạo nhiều thread
"""

import socket 
import threading

HEADER = 64  # chỉ nhận 64 byte
PORT = 5050

#IP = "192.168.1.84" #IPv4 của máy tính
IP = socket.gethostbyname(socket.gethostname()) 
    # tự lấy địa chỉ IPv4 của máy tính luôn

ADDR = (IP, PORT) 
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Khởi tạo một cái socket #TCP
server.bind((IP, PORT)) # chạy

def handle_client(conn, addr):
    """
    Hàm handle
    """
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) #
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT) #
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")  # in ra IP + tin nhắn
            conn.send("msg reveiced".encode(FORMAT)) # gửi lại client "..."

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}")
    while True:
        conn, addr = server.accept() # chờ kết nối đến. return conn and addr của client
        
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # khởi tạo thread để làm cv khác , ko ảnh hưởng vòng lặp
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") #


print("[STARTING] server is starting...")
start()
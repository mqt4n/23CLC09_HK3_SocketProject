import socket
import json
import threading
import os

FILE_LIST = 'list.json'
HOST = "127.0.0.1"
PORT = 12345
FILE_DIRECTORY = './files'
FORMAT = 'utf-8'

def load_file():
    with open(FILE_LIST, 'r') as file:
        return json.load(file)

LIST = load_file()

def file_exist(FILE_PATH):
    return os.path.isfile(FILE_PATH)

def handle_client(CLIENT_SOCKET: socket.socket, ADDR):
    print(f"Connection from {ADDR}")
    try:
        request_type = CLIENT_SOCKET.recv(1024).decode(FORMAT)
        
        if request_type == 'SEND_LIST':
            for file in LIST:
                CLIENT_SOCKET.sendall(file['filename'].encode(FORMAT))
                CLIENT_SOCKET.recv(1024).decode(FORMAT)  # Wait for ACK
                CLIENT_SOCKET.sendall(file['size'].encode(FORMAT))
                CLIENT_SOCKET.recv(1024).decode(FORMAT)  # Wait for ACK
            CLIENT_SOCKET.sendall('END_LIST'.encode(FORMAT))
        elif request_type == 'BEGIN':
            CLIENT_SOCKET.sendall('ACK'.encode(FORMAT))
            FILE_NAME = CLIENT_SOCKET.recv(1024).decode(FORMAT)
            if FILE_NAME == 'END':
                return
            CLIENT_SOCKET.sendall('ACK'.encode(FORMAT))
            priority = int(CLIENT_SOCKET.recv(1024).decode(FORMAT))
            chunk_size = 200  * priority
            file_path = os.path.join(FILE_DIRECTORY, FILE_NAME)
            if file_exist(file_path):
                CLIENT_SOCKET.sendall('START'.encode(FORMAT))

                with open(file_path, 'rb') as file:
                    while True:
                        data = file.read(chunk_size)
                        if not data:
                            break
                        CLIENT_SOCKET.sendall(data)
                CLIENT_SOCKET.sendall('END'.encode(FORMAT))
            else:
                CLIENT_SOCKET.sendall('ERROR: file not found'.encode(FORMAT))
    except Exception as e:
        print(f"Error handling client {ADDR}: {e}")
    finally:
        print(f"Closing connection with {ADDR}")
        CLIENT_SOCKET.close()

def main():
    if not os.path.exists(FILE_DIRECTORY):
        os.makedirs(FILE_DIRECTORY)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(10)
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            client_socket, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.daemon = True
            client_thread.start()

if __name__ == '__main__':
    main()



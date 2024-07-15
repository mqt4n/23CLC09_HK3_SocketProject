import os
import socket
import json

HOST = '127.0.0.1'
PORT = 12346
FILE_DIRECTORY = './files'
FILE_LIST_FILENAME = 'list.json'
FORMAT = "utf-8"

def load_file_list():
    with open(FILE_LIST_FILENAME, 'r') as f:
        return json.load(f)

FILE_LIST = load_file_list()

def file_exists(file_path):
    return os.path.isfile(file_path)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            client_socket, addr = s.accept()
            print(f"Connection from {addr}")
            try:
                for file in FILE_LIST:
                    client_socket.sendall(file['filename'].encode(FORMAT))
                    client_socket.sendall(str(file['size']).encode(FORMAT))
                client_socket.sendall('END_LIST'.encode(FORMAT))

                while True:
                    FILE_NAME = client_socket.recv(1024).decode(FORMAT)
                    if FILE_NAME == "END":
                        break

                    FILE_PATH = os.path.join(FILE_DIRECTORY, FILE_NAME)

                    if file_exists(FILE_PATH):
                        client_socket.sendall('START'.encode(FORMAT))
                        with open(FILE_PATH, 'rb') as file:
                            while True:
                                data = file.read(1024) 
                                if not data : break 
                                client_socket.sendall(data) 
                            
                        client_socket.sendall('END'.encode(FORMAT))
                    else:
                        client_socket.sendall('ERROR: File not found'.encode(FORMAT))
            except Exception as e:
                print(f"Closing connection with {addr}" )
            finally:
                client_socket.close()

if __name__ == '__main__':
    main() 


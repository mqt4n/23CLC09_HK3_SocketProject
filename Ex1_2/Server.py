import os
import socket
import json
from pathlib import Path

HOST = '192.168.1.3'
PORT = 12346
FILE_DIRECTORY = './files'
FILE_LIST_FILENAME = 'list.json'
FORMAT = "utf-8"

def convert_bytes(file_size):
	nameOfTypeData = ["B", "KB", "MB", "GB", "TB"]
	sizeOfTypeData = len(nameOfTypeData)
	for i in range(sizeOfTypeData):
		if file_size < 1024 or file_size%1024 != 0:
			return int(file_size), nameOfTypeData[i]
		file_size = file_size / 1024

def write_file_list_to_json(folder_path, output_file='list.json'):
    file_info_list = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            size, typeData = convert_bytes(file_size)
            file_info_list.append({
                "filename": file,
                "size": size, 
                "typeData": typeData
            })
    with open(output_file, 'w') as f : 
        json.dump(file_info_list, f, indent=4) 

data_path = str(Path.cwd()) + '\\files'
write_file_list_to_json(data_path, 'list.json')

def load_file_list():
    with open(FILE_LIST_FILENAME, 'r') as f:
        return json.load(f)

FILE_LIST = load_file_list()

def file_exists(file_path):
    return os.path.isfile(file_path)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            client_socket, addr = s.accept()
            print(f"Connection from {addr}")
            try:
                for file in FILE_LIST:
                    client_socket.sendall(file['filename'].encode(FORMAT))
                    client_socket.recv(1024).decode(FORMAT)
                    client_socket.sendall(str(file['size']).encode(FORMAT))
                    client_socket.recv(1024).decode(FORMAT) 
                    client_socket.sendall(file['typeData'].encode(FORMAT)) 
                    client_socket.recv(1024).decode(FORMAT)
                client_socket.sendall('END_LIST'.encode(FORMAT))

                
                while True:
                    FILE_NAME = client_socket.recv(1024).decode(FORMAT)
                    if FILE_NAME == "END":
                        break

                    FILE_PATH = os.path.join(FILE_DIRECTORY, FILE_NAME)

                    if file_exists(FILE_PATH):
                        client_socket.sendall('START'.encode(FORMAT))
                        client_socket.recv(1024).decode(FORMAT)
                        with open(FILE_PATH, 'rb') as file:
                            while True:
                                data = file.read(1024) 
                                if not data : break 
                                client_socket.sendall(data) 
                            
                        client_socket.sendall('END'.encode(FORMAT))
                    else:
                        client_socket.sendall('File not found'.encode(FORMAT))
            except Exception as e:
                print(f"Closing connection with {addr}" )
            finally:
                client_socket.close()

if __name__ == '__main__':
    main() 


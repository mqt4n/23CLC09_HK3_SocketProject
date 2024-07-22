import json
import os
import socket
import time
import signal
import sys

HOST = '127.0.0.1'
PORT = 12346
OUTPUT_DIRECTORY = 'output'
FORMAT = "utf-8"

def read_file_list_from_json(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            try:
                file_data = json.load(f)
                return file_data
            except json.JSONDecodeError: 
                return []
    return []

def file_exists(file_path):
    return os.path.isfile(file_path)

def convert_size_to_bytes(size_str):
    size_str = size_str.upper()
    if size_str.endswith('MB'):
        return int(size_str[:-2]) * 1024 * 1024
    elif size_str.endswith('GB'):
        return int(size_str[:-2]) * 1024 * 1024 * 1024
    else:
        raise ValueError("Invalid size format")

def signal_func(sig, frame):
    print("\nClient closing")
    sys.exit(0)

def main():
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        FILE_LIST_FROM_SERVER = []

        while True:
            name = s.recv(700).decode(FORMAT)
            if name == 'END_LIST':
                break
            s.sendall('ACK'.encode(FORMAT)) 
            size = s.recv(1024).decode(FORMAT)
            s.sendall('ACK'.encode(FORMAT))
            FILE_LIST_FROM_SERVER.append({'file_name': name, 'size': size})

        
        print(f"List of files from server: ")
        for file in FILE_LIST_FROM_SERVER:
            print(f"File name: {file['file_name']} | Size: {file['size']}")

        file_name = 'input.json'

        while True:
            FILE_INPUT = read_file_list_from_json(file_name)
            for file in FILE_INPUT:
                FILE_NAME = file['filename']
                SIZE = file['size']
                FILE_PATH = os.path.join(OUTPUT_DIRECTORY, FILE_NAME)

                if not file_exists(FILE_PATH):
                    s.sendall(FILE_NAME.encode(FORMAT))
                    response = s.recv(1024).decode(FORMAT)
                    
                    if response == 'START':
                        s.sendall('ACK'.encode(FORMAT))
                        with open(FILE_PATH, 'wb') as f:
                            TOTAL_SIZE = convert_size_to_bytes(SIZE)
                            RECEIVED_SIZE = 0

                            while True:
                                data = s.recv(1024)
                                if data.endswith(b'END'):
                                    f.write(data[:-3])
                                    break
                                f.write(data)
                                RECEIVED_SIZE += len(data)
                                NUMBER = round((RECEIVED_SIZE / TOTAL_SIZE) * 100 ) 
                                print(f"Downloading {FILE_NAME}: {NUMBER:.2f}% complete", end='\r')
                        print(f"\nDownload of {FILE_NAME} complete")
                    else:
                        print(response)
            time.sleep(2)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_func)
    try:
        main()
    except KeyboardInterrupt:
        print("\nClient terminated.")



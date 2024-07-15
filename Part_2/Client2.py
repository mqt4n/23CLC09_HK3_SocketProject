import json
import os
import socket
import time
import signal
import sys
import threading
from tqdm import tqdm

HOST = '127.0.0.1'
PORT = 12345
OUTPUT_DIRECTORY = 'output1'
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

def Change_priority(pri):
    if pri == 'CRITICAL':
        return 10
    elif pri == 'HIGH':
        return 4
    elif pri == 'NORMAL':
        return 1

def download_file(file):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        FILE_NAME = file['filename']
        SIZE = file['size']
        PRIORITY = file['priority']
        LEVEL = Change_priority(PRIORITY)
        FILE_PATH = os.path.join(OUTPUT_DIRECTORY, FILE_NAME)

        try:
            if not file_exists(FILE_PATH):
                s.sendall('BEGIN'.encode(FORMAT))
                s.recv(1024).decode(FORMAT)  # Receive ACK
                s.sendall(FILE_NAME.encode(FORMAT))
                s.recv(1024).decode(FORMAT) # Receive ACK \
                s.sendall(str(LEVEL).encode(FORMAT))  
                response = s.recv(1024).decode(FORMAT)
                if response == 'START':
                    with open(FILE_PATH, 'wb') as f:
                        TOTAL_SIZE = convert_size_to_bytes(SIZE)
                        RECEIVED_SIZE = 0

                        progress_bar = tqdm(total=TOTAL_SIZE, desc=f"Downloading {FILE_NAME}", unit="B", unit_scale=True, leave= False)
                        time.sleep(1)
                        while True:
                            time.sleep(0.001)
                            data = s.recv(1024)
                            if data.endswith(b'END'):
                                f.write(data[:-3])
                                progress_bar.update(len(data) - 3)
                                break
                            f.write(data)
                            RECEIVED_SIZE += len(data)
                            progress_bar.update(len(data))
                        progress_bar.close()
                else:
                    print(response)
        except Exception as e:
            print(f"Error downloading {FILE_NAME}: {e}")

def main():
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    LIST_FILE = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        s.sendall('SEND_LIST'.encode(FORMAT))
        while True:
            file_name = s.recv(1024).decode(FORMAT)
            if file_name == 'END_LIST':
                break
            s.sendall('ACK'.encode(FORMAT))
            size = s.recv(1024).decode(FORMAT)
            s.sendall('ACK'.encode(FORMAT))
            LIST_FILE.append({'filename': file_name, 'size': size})
        
        print("List of files from server:")
        for file in LIST_FILE:
            print(f"File name: {file['filename']} | Size: {file['size']}")
        
        s.close()
        threads = []
        while True:
            file_name = 'input.json'
            file_input = read_file_list_from_json(file_name)
            for file in file_input:
                thread = threading.Thread(target=download_file, args=(file,))
                thread.start()
                threads.append(thread)
            # for thread in threads:
            #     thread.join()
            time.sleep(2)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_func)
    try:
        main()
    except KeyboardInterrupt:
        print("\nClient terminated.")

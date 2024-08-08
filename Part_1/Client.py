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
nameOfTypeData = ['B','KB','MB','GB','TB']

def removeEndLine(str ) : 
	if str[len(str) - 1] == "\n" : return str[:len(str) - 1] 
	else : return str 

def readFile(FILENAME) : 
	if os.path.exists(FILENAME) : 
		data = []
		with open(FILENAME, 'r') as f : 
			try : 
				for line in f : 
					data.append(removeEndLine(line) ) 
				return data 				
			except Exception : return [] 
	else : return []


def file_exists(file_path):
    return os.path.isfile(file_path)

def convert_size_to_bytes(size, type):
    type = type.upper() 
    if type == 'MB':
        return int(size) * 1024 * 1024
    elif type == 'GB':
        return int(size) * 1024 * 1024 * 1024
    elif type == 'KB': 
         return int(size) * 1024 
    elif type == 'B' : return int(size) 
    else : 
         return int(size) 

def signal_func(sig, frame):
    print("\nClient closing")
    sys.exit(0)

def main():
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        FILE_LIST_FROM_SERVER = []
        try:
            while True:
                name = s.recv(1024).decode(FORMAT)
                if name == 'END_LIST':
                    break
                s.sendall('ACK'.encode(FORMAT)) 
                size = s.recv(1024).decode(FORMAT)
                s.sendall('ACK'.encode(FORMAT))
                type = s.recv(1024).decode(FORMAT) 
                s.sendall('ACK'.encode(FORMAT)) 
                FILE_LIST_FROM_SERVER.append({'file_name': name, 'size': size, 'typeData': type}) 

            
            print(f"List of files from server: ")
            for file in FILE_LIST_FROM_SERVER:
                if file['typeData']=='B':
                    size = int(file['size'])
                    index = 0
                    while size>=1024:
                        size/=1024
                        index+=1
                    print(f"File name: {file['file_name']} | Size: {round(size,2)} {nameOfTypeData[index]}")
                else:
                    print(f"File name: {file['file_name']} | Size: {file['size']} {file['typeData']}")

            NOT_FOUND = []
            CHECK = []
            while True: 
                file_name = 'input.txt' 
                FILE_INPUT = readFile(file_name) 
                if FILE_INPUT == CHECK : break 
                else: CHECK = FILE_INPUT 
                for file in FILE_INPUT:
                    
                    FILE_NAME = file
                    SIZE = 0 
                    TYPE = ''
                    for f in FILE_LIST_FROM_SERVER: 
                        if f['file_name'] == FILE_NAME : 
                            SIZE = f['size']  
                            TYPE = f['typeData'] 
                            
                    FILE_PATH = os.path.join(OUTPUT_DIRECTORY, FILE_NAME)

                    check = 0 
                    for i in NOT_FOUND: 
                        if i == FILE_NAME: 
                            check = 1 
                        
                    if not file_exists(FILE_PATH) and check == 0 : 
                        s.sendall(FILE_NAME.encode(FORMAT))
                        response = s.recv(1024).decode(FORMAT)
                        if response == 'START' :
                            s.sendall('ACK'.encode(FORMAT))
                            with open(FILE_PATH, 'wb') as f:
                                TOTAL_SIZE = convert_size_to_bytes(SIZE, TYPE )
                                RECEIVED_SIZE = 0
                                while True :
                                    data = s.recv(1024)
                                    RECEIVED_SIZE += len(data)
                                    if TOTAL_SIZE != 0 : 
                                        NUMBER = round((RECEIVED_SIZE / TOTAL_SIZE) * 100 ) 
                                    else : NUMBER = 100 
                                    if NUMBER >= 100 : NUMBER = 100  
                                    print(f"Downloading {FILE_NAME}: {NUMBER:.2f}% complete", end='\r')
                                    if data.endswith(b'END'):
                                        f.write(data[:-3])
                                        break
                                    f.write(data)
                            print(f"\nDownload of {FILE_NAME} complete")
                        else : 
                            print(str(FILE_NAME) + " " + response ) 
                            NOT_FOUND.append(FILE_NAME)    
        except Exception as e : 
             print("")
                

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_func)
    try:
        main()
    except KeyboardInterrupt:
        print("\nClient terminated.")

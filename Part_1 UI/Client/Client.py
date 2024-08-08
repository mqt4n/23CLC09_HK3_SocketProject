import json
import os
import socket
import time
import signal
import sys
import threading
import raySock
import globalVariable

HOST = '127.0.0.1'
PORT = 12346
OUTPUT_DIRECTORY = 'output'
FORMAT = "utf-8"
numOfFile = 0

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
    globalVariable.endProgram = True

def downloadFile(s, FILE_LIST_FROM_SERVER):
    global numOfFile
    NOT_FOUND = []
    CHECK = [] 
    while True:
        if globalVariable.endProgram == True:
            exit(0)
        file_name = 'input.txt'
        FILE_INPUT = readFile(file_name)
        if FILE_INPUT == CHECK and numOfFile != 0: 
            globalVariable.announFirst += '\nCLOSING...'
            time.sleep(2)
            globalVariable.endProgram = True
            break 
        else: CHECK = FILE_INPUT

        for file in FILE_INPUT:
            if globalVariable.announFirst.find(file) == -1:
                globalVariable.announFirst += '\n-Add ' + file + ' to download list.'            

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

            if check == 0:  
                if not file_exists(FILE_PATH): 
                    s.sendall(FILE_NAME.encode(FORMAT))
                    response = s.recv(1024).decode(FORMAT)
                    
                    if response == 'START':
                        s.sendall('ACK'.encode(FORMAT))
                        with open(FILE_PATH, 'wb') as f:
                            globalVariable.downloading = True
                            numOfFile += 1
                            TOTAL_SIZE = convert_size_to_bytes(SIZE, TYPE )
                            RECEIVED_SIZE = 0

                            while True:
                                if globalVariable.endProgram == True:
                                    exit(0)
                                data = s.recv(1024)
                                RECEIVED_SIZE += len(data)
                                if TOTAL_SIZE != 0 : 
                                    NUMBER = round((RECEIVED_SIZE / TOTAL_SIZE) * 100 ) 
                                else : NUMBER = 100 
                                if NUMBER >= 100 : NUMBER = 100   
                                globalVariable.announSecond = str(globalVariable.announFirst) + '\n' + '-Downloading ' + str(FILE_NAME) + ': ' + str(NUMBER) + "%" + " complete"  
                                if data.endswith(b'END'):
                                    f.write(data[:-3])
                                    break
                                f.write(data)
                        globalVariable.downloading = False
                        globalVariable.announFirst += '\n' + '-Downloading of ' + str(FILE_NAME) + ' complete.'
                    else : 
                        globalVariable.announFirst += '\n-' + str(FILE_NAME) + ' :FILE NOT FOUND.'
                        NOT_FOUND.append(FILE_NAME)
                else:
                    if globalVariable.announFirst.count(FILE_NAME) <= 1:
                        globalVariable.announFirst += '\n-' + str(FILE_NAME) + ' has been downloaded.'
                        numOfFile += 1

        time.sleep(2) 

def main():
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    with open('input.txt', 'w') as f:       
        f.write('')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        globalVariable.init()
        FILE_LIST_FROM_SERVER = []

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
        
        thr1 = threading.Thread(target = raySock.makeConsoleWindow, args = (FILE_LIST_FROM_SERVER,))
        thr1.deamon = True
        thr1.start()

        thr2 = threading.Thread(target = downloadFile, args = (s,FILE_LIST_FROM_SERVER,))
        thr2.deamon = True
        thr2.start()    

        while globalVariable.endProgram != True:    
            # do something
            temp = 1

                    
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_func)
    try:
        main()
    except KeyboardInterrupt:
        print("\nClient terminated.")



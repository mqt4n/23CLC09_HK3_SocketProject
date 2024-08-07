import socket
import signal
import sys

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def main():

    HOST = "127.0.0.1" # The server's hostname or IP address
    PORT = 65432 # The port used by the server
    FORMAT = "utf8"
    nameTypeOfData = ["B","KB","MB","GB","TB"]
    BUFSIZE = 1024
    ACK = ""

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("CLIENT SIDE")
    client.connect((HOST, PORT))
    print("client address:", client.getsockname())

    # Receive the content of the JSON file from the server
    file_list = []
    sizeOfFileList = int(client.recv(BUFSIZE).decode(FORMAT))

    while sizeOfFileList > 0:
        temp = {
        "filename": "file1.txt",
        "size": 1024,
        "typeData": "KB"
        }
        temp["filename"] = client.recv(BUFSIZE).decode(FORMAT)
        client.send("ACK".encode(FORMAT))
        temp["size"] = float(client.recv(BUFSIZE).decode(FORMAT))
        client.send("ACK".encode(FORMAT))
        temp["typeData"] = client.recv(BUFSIZE).decode(FORMAT)
        client.send("ACK".encode(FORMAT))
        file_list.append(temp)
        sizeOfFileList -= 1
        
    # Print the content of the JSON file
    for items in file_list:
        if items['typeData'] == "B":
            size = int(items['size'])
            index = 0
            while size >= 1024:
                size = size / 1024
                index += 1
            print(f"File name: {items['filename']}, File size: {size:.2f} {nameTypeOfData[index]}")
        else:
            print(f"File name: {items['filename']}, File size: {items['size']} {items['typeData']}")

    data_require_before = []
    data_require_after = []
    while True:
        try: 
            # Sent required data to the server    
            fi = open("input.txt", "r")
            data_require_after = fi.readlines()
            fi.close()
            sizeBefore = len(data_require_before)
            sizeAfter = len(data_require_after)
            
            if sizeBefore == sizeAfter:
                break
            
            data_require_after = data_require_after[sizeBefore:]
            client.send(str(len(data_require_after)).encode(FORMAT))
            ACK = client.recv(BUFSIZE).decode(FORMAT)

            for i in range(len(data_require_after)):
                if data_require_after[i] == "": continue
                if data_require_after[i][len(data_require_after[i]) - 1] == "\n":
                    data_require_after[i] = data_require_after[i][:len(data_require_after[i]) - 1]
                client.send(data_require_after[i].encode(FORMAT))
                ACK = client.recv(BUFSIZE).decode(FORMAT)

            print("\n")

            while len(data_require_after) > 0:
                sizeDownLoad = client.recv(BUFSIZE).decode(FORMAT)
                
                if sizeDownLoad == "-1":
                    print(f"Server don't have {data_require_after[0]}!", end = "")
                    client.send("ACK".encode(FORMAT))
                    data_require_before.append(data_require_after[0])
                    data_require_after.pop(0)
                    continue
                
                sizeDownLoad = float(sizeDownLoad)
                client.send("ACK".encode(FORMAT))
                fo = open("output/"+data_require_after[0], "wb")
                toTalSize = sizeDownLoad
                
                while sizeDownLoad > 0:
                    data = client.recv(BUFSIZE)
                    client.send("ACK".encode(FORMAT))
                    fo.write(data)
                    sizeDownLoad -= len(data)
                    percentage = round((1 - sizeDownLoad/toTalSize) * 100, 2)
                    print(f"Downloading {data_require_after[0]}... {percentage}%", end = "\r")
                fo.close()
                data_require_before.append(data_require_after[0])
                data_require_after.pop(0)  
                print("\n")
                
        except:
            print("Closing connection!")
            client.close()
            break
        
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
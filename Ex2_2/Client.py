import os
import sys
import time
import socket
import signal
import raySock
import threading
import globalVariable

HOST = "10.124.7.166" # The server's hostname or IP address
PORT = 65432 # The port used by the server
FORMAT = "utf-8"
nameTypeOfData = ["B","KB","MB","GB","TB"]
BUFSIZE = 1024
ACK = ""
modeName = ["NORMAL", "HIGH", "CRITICAL"]
modeDownLoad = [1, 4, 10]
output_folder = 'output'
scanTime = 2

timeToScan = [0, 0]

def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Program will exit!')
    globalVariable.endProgram = True    
    time.sleep(1)

def timer(): 
    global timeToScan
    while True: 
        if globalVariable.endProgram == True : break 
        time.sleep(1) 
        timeToScan[1] += 1

def printPercentage(lengthOfEachFile, total_lengOfEachFile, file_pointer):
    temp = ''
    for items in file_pointer:
        percent = round(((1 - lengthOfEachFile[file_pointer.index(items)] / total_lengOfEachFile[file_pointer.index(items)])) * 100, 2)
        if percent == 100:  
            if globalVariable.announFirst.find(items.name) == -1: 
                globalVariable.announFirst += '\n-Download ' + str(items.name) + ' successfully.'
            else:
                continue
        else:
            temp += '\n-Downloading ' + str(items.name) + ': ' + str(percent) + '%'
    globalVariable.announSecond = globalVariable.announFirst + temp

def fillterDataNotFoundAndPrint(list404, list_file_not_found):
    for items in list404:
        check = False
        for key in list_file_not_found:
            if items == key:
                check = True
                break
        if check == False:
            list_file_not_found.append(items)
            globalVariable.announFirst += '\n-File ' + str(items['filename']) + ' not found in the list'

def fillterData(data, file_list, list404, list_download):
    for items in data:
        check = False
        for i in range(len(file_list)):
            if items["filename"].strip() == file_list[i]["filename"]:
                list_download.append(items)
                check = True
                break
        if check == False:
            list404.append(items)

def readRequiredData(file_path):
    data = []
    with open(file_path, "r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            idxSpace = line.find(" ")
            if idxSpace != -1:
                temp = {}
                temp["filename"] = line[:idxSpace]
                temp["mode"] = removeEndLine(line[idxSpace + 1:])
                data.append(temp)
    return data

def setLengthOfEachFile(data_require, file_list, lengthOfEachFile, total_lengOfEachFile):
    for items in data_require:
        size = 0
        for i in range(len(file_list)):
            if items["filename"].strip() == file_list[i]["filename"]:
                size = file_list[i]["size"]
                break
        lengthOfEachFile.append(size)
        total_lengOfEachFile.append(size)

def removeEndLine(str):
	if str[len(str) - 1] == "\n":
		return str[:len(str) - 1]
	return str

def UpLoadProcess(lengthOfEachFile):
    for x in lengthOfEachFile:
        if x != 0:
            return False        
    return True

def downloadFile(file_list, client):
    # Convert the size of each file to bytes
    for i in range(len(file_list)):
        for j in range(len(nameTypeOfData)):
            if file_list[i]["typeData"] == nameTypeOfData[j]:
                file_list[i]["size"] = file_list[i]["size"] * (1024 ** j)
                break
    
    data_require_before = []
    list_file_not_found = []
    total_file = 0
    
    try:
        # set the time to read file 
        thread = threading.Thread(target = timer , args = ()) 
        thread.daemon = True 
        thread.start()
        
        global timeToScan
        while True:
            if globalVariable.endProgram == True: break
            # Load required data from the input.txt file 
            #Remove end line of each line 
            if(timeToScan[1] - timeToScan[0] < scanTime):
                continue
            else: 
                timeToScan[0] = timeToScan[1] 
            data_require_after = readRequiredData("input.txt")
            
            total_file = len(data_require_after)
            
            #Remove file not in the list
            list404 = []
            list_download = []
            
            #Fillter data
            fillterData(data_require_after, file_list, list404, list_download)
                    
            data_require_after = list_download
            
            fillterDataNotFoundAndPrint(list404, list_file_not_found)
            
            sizeBefore = len(data_require_before)
            sizeAfter = len(data_require_after)
            
            if sizeBefore == sizeAfter:
                continue

            # Send the required data to the server
            data_require_after = data_require_after[sizeBefore:]
            client.send(str(len(data_require_after)).encode(FORMAT))
            ACK = client.recv(BUFSIZE).decode(FORMAT)

            for i in range(len(data_require_after)):
                client.send(data_require_after[i]["filename"].encode(FORMAT))
                ACK = client.recv(BUFSIZE).decode(FORMAT)
                client.send(data_require_after[i]["mode"].encode(FORMAT))
                ACK = client.recv(BUFSIZE).decode(FORMAT)

            # Receive the required data from the server
            file_pointer = []
            for items in data_require_after:
                file_pointer.append(open("output/"+items["filename"], "wb"))
                
                
            lengthOfEachFile = []
            total_lengOfEachFile = []
            setLengthOfEachFile(data_require_after, file_list, lengthOfEachFile, total_lengOfEachFile)
                
            # #print percentage of each file download    
            for items in data_require_after:
                globalVariable.announFirst += '\n-Downloading ' + str(items['filename']) + ' with mode ' + str(items['mode'])
          
            
            while UpLoadProcess(lengthOfEachFile) == False:
                globalVariable.downloading = True
                for items in file_pointer:
                    if lengthOfEachFile[file_pointer.index(items)] <= 0:
                        continue
                    modeNumer = 1
                    for i in range(len(modeName)):
                        if data_require_after[file_pointer.index(items)]["mode"] == modeName[i]:
                            modeNumer = modeDownLoad[i]
                            break
                    for i in range(modeNumer):
                        if lengthOfEachFile[file_pointer.index(items)] <= 0:
                            continue
                        client.send("ACK".encode(FORMAT))
                        data = client.recv(BUFSIZE)
                        items.write(data)
                        lengthOfEachFile[file_pointer.index(items)] -= len(data)
                
                printPercentage(lengthOfEachFile, total_lengOfEachFile, file_pointer)                

                if(timeToScan[1] - timeToScan[0] < scanTime):
                    client.send("0".encode(FORMAT))
                    client.recv(BUFSIZE).decode(FORMAT)
                    continue
                else : timeToScan[0] = timeToScan[1]

                
                update_data_require_after = readRequiredData("input.txt")
                
                total_new_file = len(update_data_require_after) - total_file
                
                if total_new_file <= 0:
                    client.send("0".encode(FORMAT))
                    ACK = client.recv(BUFSIZE).decode(FORMAT)
                    continue
                    
                update_data_require_after = update_data_require_after[total_file:]
                
                #Remove file not in the list
                new_list404 = []
                new_list_download = []
                fillterData(update_data_require_after, file_list, new_list404, new_list_download)
                
                update_data_require_after = new_list_download
                
                #print file not in the list
                fillterDataNotFoundAndPrint(new_list404, list_file_not_found)
                
                #check need to download new file or not
                if len(update_data_require_after) == 0:
                    total_file += total_new_file
                    client.send("0".encode(FORMAT))
                    ACK = client.recv(BUFSIZE).decode(FORMAT)
                    continue
                
                #Send new required file to the server
                client.send(str(len(update_data_require_after)).encode(FORMAT))
                ACK = client.recv(BUFSIZE).decode(FORMAT)
                
                #Print notification for new required file
                for items in update_data_require_after:
                    globalVariable.announFirst += '\n-Downloading ' + str(items['filename']) + ' with mode ' + str(items['mode'])
                    data_require_after.append(items)  
                
                for i in range(len(update_data_require_after)):
                    client.send(update_data_require_after[i]["filename"].encode(FORMAT))
                    ACK = client.recv(BUFSIZE).decode(FORMAT)
                    client.send(update_data_require_after[i]["mode"].encode(FORMAT))
                    ACK = client.recv(BUFSIZE).decode(FORMAT)

                # Make the list file pointer
                for items in update_data_require_after:
                    file_pointer.append(open("output/"+items["filename"], "wb"))
                    
                #Set the length of each new file    
                setLengthOfEachFile(update_data_require_after, file_list, lengthOfEachFile, total_lengOfEachFile)
                    
                total_file += total_new_file
#----------------------------------------------------------------------------------------------
            globalVariable.downloading = False
            for items in file_pointer:
                items.close()
                
            for items in data_require_after:
                data_require_before.append(items)
                        
    except Exception as e:
        client.close()


    
def main():
    globalVariable.init()
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open('input.txt', 'w') as f:
        f.write('')

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("CLIENT SIDE")
    client.connect((HOST, PORT))
    print("client address:", client.getsockname())

    # Receive the content of the JSON file from the server
    file_list = []
    sizeOfFileList = int(client.recv(BUFSIZE).decode(FORMAT))
    print("\nNumber of file in list: ", sizeOfFileList)
    
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

    thr1 = threading.Thread(target = raySock.makeConsoleWindow, args = (file_list,))
    thr1.deamon = True
    thr1.start()

    thr2 = threading.Thread(target = downloadFile, args = (file_list, client,))
    thr2.deamon = True
    thr2.start()    

    while True:
        if globalVariable.endProgram == True:
            break

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()


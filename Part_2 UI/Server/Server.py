import socket
import threading
import json
import os
from pathlib import Path

HOST = "127.0.0.1" # The server's hostname or IP address
PORT = 65432 # The port used by the server
FORMAT = "utf-8"
BUFSIZE = 1024
data_path = str(Path.cwd()) + '\\files'
file_path = "file_list.json"
nameTypeOfData = ["B","KB","MB","GB","TB"]
sizeTypeOfData = len(nameTypeOfData)
modeName = ["NORMAL", "HIGH", "CRITICAL"]
modeDownLoad = [1, 4, 10]

def convert_bytes(file_size):
	nameOfTypeData = ["B", "KB", "MB", "GB", "TB"]
	sizeOfTypeData = len(nameOfTypeData)
	for i in range(sizeOfTypeData):
		if file_size < 1024 or file_size%1024 != 0:
			return file_size, nameOfTypeData[i]
		file_size = file_size / 1024

def write_file_list_to_json(folder_path, output_file='file_list.json'):
    # List to hold file information
    file_info_list = []

    # Walk through the directory
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Get the full file path
            file_path = os.path.join(root, file)
            # Get the file size in MB
            file_size = os.path.getsize(file_path)
            size, typeData = convert_bytes(file_size)
            # Append file information to the list
            file_info_list.append({
                "filename": file,
                "size": size, 
                "typeData": typeData
            })

    # Write the list to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(file_info_list, json_file, indent=4)

def setLengthOfEachFile(data_require, file_list, lengthOfEachFile, nameTypeOfData):
    for items in data_require:
        for i in range(len(file_list)):
            if file_list[i]['filename'] == items["filename"]:
                for j in range(len(nameTypeOfData)):
                    if file_list[i]['typeData'] == nameTypeOfData[j]:
                        lengthOfEachFile.append(int(file_list[i]['size'] * (1024 ** j)))
                        break
                break

def UpLoadProcess(lengthOfEachFile):
    for x in lengthOfEachFile:
        if x != 0:
            return False
    return True

def handle_client(connection, address, file_list):
	while True:
		try:
      
			print("client address: ", address)
			print("connection: ", connection.getsockname(), end="\n\n")
			print("Server is connected to the client")
			
			connection.send(str(len(file_list)).encode(FORMAT))
			for items in file_list:
				connection.send(items['filename'].encode(FORMAT))
				ACK = connection.recv(BUFSIZE).decode(FORMAT)
				connection.send(str(items['size']).encode(FORMAT))
				ACK = connection.recv(BUFSIZE).decode(FORMAT)
				connection.send(items['typeData'].encode(FORMAT))
				ACK = connection.recv(BUFSIZE).decode(FORMAT)
			
			try:
				while True:
					data_require = []
					# Receive the required data from the client
					sizeOfDataRequire = int(connection.recv(BUFSIZE).decode(FORMAT))
					connection.send("ACK".encode(FORMAT))

					while sizeOfDataRequire > 0:
						temp = {}
						temp["filename"] = connection.recv(BUFSIZE).decode(FORMAT)
						connection.send("ACK".encode(FORMAT))
						temp["mode"] = connection.recv(BUFSIZE).decode(FORMAT)
						connection.send("ACK".encode(FORMAT))
						data_require.append(temp)
						sizeOfDataRequire -= 1

					# Print the required data
					print("Data required from the client with address: ", address)
					for items in data_require:
						print(f"File name: {items['filename']}, Mode: {items['mode']}")

					# Set the length of each file
					lengthOfEachFile = []
					setLengthOfEachFile(data_require, file_list, lengthOfEachFile, nameTypeOfData)

					# Make the list file pointer
					file_pointer = []
					for items in data_require:
						path = data_path + "\\" + items["filename"]
						file_pointer.append(open(path, "rb"))
					
					# Send the required data to the client
					while UpLoadProcess(lengthOfEachFile) == False:
						for items in file_pointer:
							if lengthOfEachFile[file_pointer.index(items)] <= 0:
								continue
							modeNumer = 1
							for i in range(len(modeName)):
								if data_require[file_pointer.index(items)]["mode"] == modeName[i]:
									modeNumer = modeDownLoad[i]
									break
							for i in range(modeNumer):
								if lengthOfEachFile[file_pointer.index(items)] <= 0:
									continue
								buffer = items.read(BUFSIZE)
								ACK = connection.recv(BUFSIZE).decode(FORMAT)
								connection.send(buffer)
								lengthOfEachFile[file_pointer.index(items)] -= len(buffer)
						
						total_new_items = int(connection.recv(BUFSIZE).decode(FORMAT))
						connection.send("ACK".encode(FORMAT)) 
						
						if total_new_items == 0:
							continue
						
						new_require_data = []
						
						while total_new_items > 0:
							temp = {}
							temp["filename"] = connection.recv(BUFSIZE).decode(FORMAT)
							connection.send("ACK".encode(FORMAT))
							temp["mode"] = connection.recv(BUFSIZE).decode(FORMAT)
							connection.send("ACK".encode(FORMAT))
							new_require_data.append(temp)
							total_new_items -= 1
							
						print("Data required from the client with address: ", address)
						for items in new_require_data:
							print(f"File name: {items['filename']}, Mode: {items['mode']}")
							data_require.append(items)
						
						# Set the length of each file
						setLengthOfEachFile(new_require_data, file_list, lengthOfEachFile, nameTypeOfData)

						# Make the list file pointer
						for items in new_require_data:
							path = data_path + "\\" + items["filename"]
							file_pointer.append(open(path, "rb"))
							
					for item in file_pointer:
						item.close()
						
					print(f"\nAll files are sent to the client has address {address}!\n")

			except Exception as e:
				print(f"Error: {e}")
				break

		except Exception as e:
			print(f"Connection with the client has address {address} is closed!")
			break
  
def main():
	write_file_list_to_json(data_path, file_path)
	# Open the JSON file and load its content
	with open(file_path, "r") as file:
		data = json.load(file)

	#Create a server socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((HOST, PORT))
	server.listen()

	print("SERVER SIDE")
	print(f"Server is listening on {HOST}:{PORT}")

	print("Sever is waiting for client request...\n")

	while True:
		connection, address = server.accept()
		thread = threading.Thread(target=handle_client, args=(connection, address, data))
		thread.daemon = False
		thread.start()
 
if __name__ == "__main__":
	main()
	input("Press Enter to continue...")



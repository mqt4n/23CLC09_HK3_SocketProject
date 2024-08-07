import socket
import json
import os

data_path = "./files"
file_path = "list.json"
HOST = "127.0.0.1" # The server's hostname or IP address
PORT = 65432 # The port used by the server
FORMAT = "utf8"
BUFSIZE = 1024
nameTypeOfData = ["B","KB","MB","GB","TB"]
sizeTypeOfData = len(nameTypeOfData)

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

write_file_list_to_json(data_path, 'list.json')

def main():
	# Open the JSON file and load its content
	with open(file_path, "r") as file:
		data = json.load(file)

	#Create a server socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((HOST, PORT))
	server.listen()

	print("SERVER SIDE")
	print(f"Server is listening on {HOST}:{PORT}")


	while True:
		
		print("\nSever is waiting for client request...")
	
		connection, address = server.accept()
		print("client address: ", address)
		print("connection: ", connection.getsockname(),end = "\n\n")

		# Open the JSON file and load its content
		ACK = ""
		connection.send(str(len(data)).encode(FORMAT))
		for items in data:
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
					data_require.append(connection.recv(BUFSIZE).decode(FORMAT))
					connection.send("ACK".encode(FORMAT))
					sizeOfDataRequire -= 1

				# Print the required data
				print("Data required:")
				print(data_require)

				while len(data_require) > 0:
					sizeUpLoad = -1
					idx_file = -1
					for i in range(len(data)):
						if data[i]["filename"] == data_require[0]:
							sizeUpLoad = data[i]["size"]
							idx_file = i
							
					if sizeUpLoad == -1:
						connection.send("-1".encode(FORMAT))
						ACK = connection.recv(BUFSIZE).decode(FORMAT)
						print(f"File {data_require[0]} is not found!")
						data_require.pop(0)
						continue
					
					for i in range(sizeTypeOfData):
						if data[idx_file]["typeData"] == nameTypeOfData[i]:
							sizeUpLoad *= 1024 ** i
							break
						
					connection.send(str(sizeUpLoad).encode(FORMAT))
					ACK = connection.recv(BUFSIZE).decode(FORMAT)
					sizeDown = sizeUpLoad
					index = 0
					while sizeDown >= 1024:
						sizeDown = sizeDown / 1024
						index += 1
					print(f"Uploading {data_require[0]} with size {sizeDown:.2f} {nameTypeOfData[index]}...")
					fi = open("files/"+data_require[0], "rb")
					
					while sizeUpLoad>0:
						buffer = fi.read(BUFSIZE)
						connection.send(buffer)
						connection.recv(BUFSIZE).decode(FORMAT)
						sizeUpLoad -= BUFSIZE
					fi.close()
					print(f"Upload successfully {data_require[0]}!")
					data_require.pop(0)
		except:
			print("Client disconnected!")
			connection.close()
			continue
					

if __name__ == "__main__":
	main()
#import required modules

from multiprocessing.connection import Client
import socket
import threading
import os
import time
from tkinter import *
from tkinter import filedialog
import pyautogui as pag
import os, shutil
from PIL import Image
address = 0
m = 0
data = ""
data1 = ''



HOST = '127.0.0.1'
#HOST = '127.0.0.1'
# '192.168.43.39'
#use between 0to 65535
#PORT = int(input("Enter the port number for chat room its a four digit number"))
PORT = 12000
LISTENER_LIMIT = 5
active_clients = [] #list of allcurrently connected users

#functions to listen for upcoming messages from a client
def listen_for_messages(client, username):
	while 1:
		message = client.recv(2048).decode('utf-8')
		if message == "send_file":
			recive_msg(client)
			#send_file(client)
			
		if message != '':
			final_msg = username+ "~"+message
			send_messages_to_all(final_msg)
		else:
			print(f"The msg sent from the client {username} is empty")	
#function to send messgae to a single client
def send_messages_to_client(client, message):
	client.sendall(message.encode())

#function to send any new messages to all the clients that are currently connected to this server
def send_messages_to_all(message):
	for user in active_clients:
		send_messages_to_client(user[1], message)

#function to ahndle client
def client_handler(client):
	#server will listens for client messeage that will contain the username
	while 1:
		username = client.recv(2048).decode('utf-8')	
		if username != '':
			active_clients.append((username,client))
			prompt_message="SERVER~"+f"{username} added to added to the chat"
			send_messages_to_all(prompt_message)
			break
		else:
			print("client username is empty")

	threading.Thread(target=listen_for_messages, args=(client, username, )).start()

def send_file(client,file_name,file_size):
	file_name = client.send(2048).decode('utf-8')
	file_size = client.send(2048).decode('utf-8')

	with open(file_name+"1", "rb") as file:
		c = 0
		# Starting the time capture.
		start_time = time.time()

		# Running the loop while file is recieved.
		while c <= int(file_size):
			data = client.sendall(2048).encode('utf-8')
			if not (data):
				break
			#file.write(data)
			client.send(data)
			#send_messages_to_all(data)
			c += len(data)

		# Ending the time capture.
		end_time = time.time()

	print("File transfer Complete.Total time: ", end_time - start_time)
	#client.sendall("Finish".encode("utf-8"))



def recive_msg(client):
	file_name = client.recv(2048).decode('utf-8')
	file_size = client.recv(2048).decode('utf-8')

	with open(file_name + "1" , "wb") as file:
		c = 0
		# Starting the time capture.
		start_time = time.time()

		# Running the loop while file is recieved.
		while c <= int(file_size):
			data = client.recv(2048).decode('utf-8')
			if not (data):
				break
			file.write(data)
			#client.sendall(data)
			#send_messages_to_all(data)
			c += len(data)

		# Ending the time capture.
		end_time = time.time()
	file_name1 = file_name + "1"
	send_file(client,file_name1,file_size)
	print("File transfer Complete.Total time: ", end_time - start_time)

def main():
	#creating the socket class object
	#AF_INET -> using IPv4 addresses
	#SOCK_DGRAM -> udp
	#SOCK_STREAM = > TCP
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	#creating a try catch block
	try:	
	#provide the server with an server form of host ip address and port
		server.bind((HOST, PORT))	
		print(f"Running the server on {HOST} {PORT}")
	except:
		print("unable to bind to host {HOST} and port {PORT}")

	#set server limit
	server.listen(LISTENER_LIMIT)
	
	#while loop keeps listening to client connections
	while 1:
		client, address = server.accept()	
		print(f"Sucessfully connected to client{address[0]} {address[1]}")
		threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
	main()

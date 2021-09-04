50#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import sys 


def proxy(tcpSocket):
	originalData = tcpSocket.recv(1024)
	splitData = originalData.split()

	website = str(splitData[4],"UTF-8")

	print(website)

	proxyConnection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	
	theAddress = socket.gethostbyname(website)
	print(theAddress)
	proxyConnection.connect((theAddress, 80))
	print("connected")
	proxyConnection.sendall(originalData)
	print("sended")
	proxyConnection.settimeout(1)
	while True:
		try:
			dataFromClient = proxyConnection.recv(1024)
			if len(dataFromClient)>0:
				tcpSocket.send(dataFromClient)
		except socket.timeout:
			break
	tcpSocket.close()
	print("wtf")
	proxyConnection.close()


def startServer(serverAddress, serverPort):
	# 1. Create server socket
	socketFromServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# 2. Bind the server socket to server address and server port
	socketFromServer.bind((serverAddress,serverPort))
	# 3. Continuously listen for connections to server socket
	while True:
		try:
			socketFromServer.listen()
			print("The server is listening....")
			client,addr = socketFromServer.accept()
			print("connection has been established with: " , addr)
			proxy(client)
		except KeyboardInterrupt:
			socketFromServer.close()
	# 4. When a connection is accepted, call handleRequest function, passing new connection socket (see https://docs.python.org/3/library/socket.html#socket.socket.accept)
	#socketTCP = socket.socket(socket.AF_INET, socket.SOCK_RAW,socket.getprotobyname("tcp"))
	# 5. Close server socket
	


startServer("127.0.0.1", 8001)
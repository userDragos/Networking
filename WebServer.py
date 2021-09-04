#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import sys 


def handleRequest(tcpSocket):
	# 1. Receive request message from the client on connection socket
	data = tcpSocket.recv(1024).split()
	# 2. Extract the path of the requested object from the message (second part of the HTTP header)
	# 3. Read the corresponding file from disk
	req = str(data[1],"UTF-8")
	requestedPath = req.replace("/", "")
	
	print(requestedPath)
	
	# 4. Store in temporary buffer
	# 5. Send the correct HTTP response error
	try:
		f = open(requestedPath,"r").read()
		#tcpSocket.send(bytes("200","UTF-8"))
		tcpSocket.send(bytes("HTTP/1.1 200 OK\r\n", "UTF-8"))
		tcpSocket.send(bytes("Content-Type:text/html\n\n","UTF-8"))
		tcpSocket.send(bytes(f, "UTF-8"))
		# 6. Send the content of the file to the socket
		# 7. Close the connection socket 
		
	except IOError:
		tcpSocket.send(bytes("HTTP/1.1 404 The file is not found", "UTF-8"))
	tcpSocket.close()
def startServer(serverAddress, serverPort):
	# 1. Create server socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# 2. Bind the server socket to server address and server port
	sock.bind((serverAddress,serverPort))
	# 3. Continuously listen for connections to server socket
	while True:
		try:
			sock.listen()
			client,addr = sock.accept()
			print("connection has been established with: " , addr)
			handleRequest(client)
		except KeyboardInterrupt:
			socketFromServer.close()
		# 4. When a connection is accepted, call handleRequest function, passing new connection socket (see https://docs.python.org/3/library/socket.html#socket.socket.accept)
		#socketTCP = socket.socket(socket.AF_INET, socket.SOCK_RAW,socket.getprotobyname("tcp"))
		
	# 5. Close server socket
	sock.close()


startServer("127.0.0.1", 8001)
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import os
import sys
import struct
import time
import select
import binascii  


ICMP_ECHO_REQUEST = 8 #ICMP type code for echo request messages
ICMP_ECHO_REPLY = 0 #ICMP type code for echo reply messages
sendingTime=0
ttl=1
sequenceNumber = 0

def checksum(string): 
	csum = 0
	countTo = (len(string) // 2) * 2  
	count = 0

	while count < countTo:
		thisVal = string[count+1] * 256 + string[count]
		csum = csum + thisVal 
		csum = csum & 0xffffffff  
		count = count + 2
	
	if countTo < len(string):
		csum = csum + string[len(string) - 1]
		csum = csum & 0xffffffff 
	
	csum = (csum >> 16) + (csum & 0xffff)
	csum = csum + (csum >> 16)
	answer = ~csum 
	answer = answer & 0xffff 
	answer = answer >> 8 | (answer << 8 & 0xff00)

	answer = socket.htons(answer)

	return answer
def receiveOnePing(icmpSocket, destinationAddress, ID, timeout):
	while True:
		# 1. Wait for the socket to receive a reply
		ready = select.select([icmpSocket],[],[],timeout)
		# 2. Once received, record time of receipt, otherwise, handle a timeout
		receiveTime= time.time()
		if ready[0] ==[]:
			return
		
		receivedPacket, address = icmpSocket.recvfrom(1024)
		header = receivedPacket[20:28]
		print(address)
		# 3. Compare the time of receipt to time of sending, producing the total network delay
		# 4. Unpack the packet header for useful information, including the ID
		type,code,checksum,Id,sequence = struct.unpack("bbHHh" , header)
		# 5. Check that the ID matches between the request and reply
		# 6. Return total network delay
		if Id == ID:
			return (receiveTime - sendingTime) * 1000
	
def sendOnePing(icmpSocket, destinationAddress, ID):
	global sequenceNumber
	global sendingTime
	dest = socket.gethostbyname(destinationAddress)
	# 1. Build ICMP header
	header = struct.pack("bbHHh",ICMP_ECHO_REQUEST,0, 0, ID , sequenceNumber)
	# 2. Checksum ICMP packet using given function
	check = checksum(header)
	# 3. Insert checksum into packet
	header = struct.pack("bbHHh",ICMP_ECHO_REQUEST,0, check, ID , sequenceNumber)
	# 4. Send packet using socket
	icmpSocket.sendto(header,(dest,1))
	# 5. Record time of sending
	
	sendingTime = time.time()
	
	sequenceNumber = sequenceNumber+1
	
def doOnePing(destinationAddress, timeout): 
	global ttl
	# 1. Create ICMP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,socket.getprotobyname("icmp"))
	host = socket.gethostbyname(destinationAddress)
	setTTL = sock.setsockopt(socket.IPPROTO_IP,socket.IP_TTL,ttl)
	# 2. Call sendOnePing function
	sendOnePing(sock, host, 15)
	# 3. Call receiveOnePing function
	delay = receiveOnePing(sock, host,15, timeout)
	# 4. Close ICMP socket
	sock.close()
	# 5. Return total network delay
	return delay
	
	
def ping(host, timeout=1):
	while True:
		try:
			global ttl
			try:
				delay = "{0:.3f}".format(doOnePing(host, timeout))
				ipAddress = socket.gethostbyname(host)
				print(host,"(",ipAddress,"): ","sequence=",sequenceNumber ," time=",delay)
				break
			except:
				if (ttl < 64):
					ttl = ttl+1
					print("sequence=",sequenceNumber)
				else:
					print("The address is unreachable")
					break
		except KeyboardInterrupt:
			break
		# 1. Look up hostname, resolving it to an IP address
		# 2. Call doOnePing function, approximately every second
		# 3. Print out the returned delay
		# 4. Continue this process until stopped	
	

ping("imperial.ac.uk")


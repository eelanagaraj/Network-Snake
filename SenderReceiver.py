#!/usr/bin/python
import socket
import time
import Queue
import threading
""" two way communication:
		Send packets to 127.0.0.1 from port 4000 to 4001"""
import socket



## listener waits for packets, when received puts them in queue q
def listener(UDP_IP, UDP_PORTin, q,):
	#receiver: must bind to given listening address, will then listen for packets in loop later on
	receiver = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

	receiver.bind((UDP_IP, UDP_PORTin))
	# sender.bind((UDP_IP, UDP_PORTout))

	# we listen for packets and send them to the game thread
	while True:
		data, addr = receiver.recvfrom(512) # buffer size is 1024 bytes
		print data
		q.put(data)

# Sender listens to the queue q, when the latter contains a packet it sends it to Friend at port UDP_PORTout
# will stop after 10 iterations, c.f. count
def sender(FriendUDP_IP, UDP_PORTout,q,b,):
	# sender: creating socket that will send over Internet using UDP protocol
	sender = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

	count = 1
	while True:
		time.sleep(1)
		if q.qsize() > 0 and count < 10:
			received = q.get()
			MESSAGE = received[:-2]+ str(count)+b
			sender.sendto(MESSAGE, (FriendUDP_IP, UDP_PORTout))
			count += 1
		elif count >= 10:
			break


UDP_IP = "10.251.54.174"
EelaUDP_IP = "10.251.54.255"
UDP_PORTout = 4000
UDP_PORTin = 4001
Qs = Queue.Queue()
Qc = Queue.Queue()

receiveServer = threading.Thread(target= listener, args = (UDP_IP,UDP_PORTin,Qs,))
sendServer = threading.Thread(target= sender, args = (UDP_IP, UDP_PORTout,Qs,'S',))
receiveClient = threading.Thread(target= listener, args = (UDP_IP,UDP_PORTout,Qc,))
sendClient = threading.Thread(target= sender, args = (UDP_IP, UDP_PORTin,Qc,'C',))

sendServer.start()
receiveServer.start()
sendClient.start()
receiveClient.start()

## We inject a packet to start message looping
# sender: creating socket that will send over Internet using UDP protocol
sender = socket.socket(socket.AF_INET, # Internet
                 socket.SOCK_DGRAM) # UDP

MESSAGE = "waddup0S" 
sender.sendto(MESSAGE, (UDP_IP, UDP_PORTout))



sendServer.join()
receiveServer.join()
sendClient.join()
receiveClient.join()

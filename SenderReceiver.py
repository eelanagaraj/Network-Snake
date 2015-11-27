#!/usr/bin/python
import socket
import time
import Queue
import threading
import socket
""" two way communication stuff:
		Send packets to 127.0.0.1 from port 4000 to 4001"""



def listener(UDP_IP, UDP_PORTin, q,):
	## We listen on port UDP_PORTin, at ip UDP_IP for udp packets that we then push to our 
	## queue q 

	#receiver: must bind to given listening address, will then listen for packets in loop later on
	receiver = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
	receiver.bind((UDP_IP, UDP_PORTin))
	# sender.bind((UDP_IP, UDP_PORTout))

	# we listen for packets and send them to the game thread/ put them in the queue
	while True:
		data, addr = receiver.recvfrom(512) # buffer size is 1024 bytes
		print data
		q.put(data)
		time.sleep(1)


def sender(FriendUDP_IP, UDP_PORTout,q,b,):
	## Sender: listens to a queue q, pulls a packet if queue is not empty and
	## sends it to FriendUDP_IP at port UDP_PORTout

	# sender: creating socket that will send over Internet using UDP protocol
	sender = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

	while True:
		if q.qsize() > 0:#and count < 10:
			packet = q.get()
			sender.sendto(packet, (FriendUDP_IP, UDP_PORTout))
			print 'sent' + b + '\n'


def packetcrafter(qi, qo):
	## function that listens to a queue qi, pulls any pushed packets, crafts
	## response packets and psuhes them to qo
	while True: 
		if qi.qsize() > 0:
			received = qi.get()
			print 'received'
			count = received[-1]
			packet = str(time.time())+ "____" + str(int(count) + 1)
			qo.put(packet)


UDP_IP = "192.168.1.161"
UDP_PORTout = 4000
UDP_PORTin = 4001

Qsi = Queue.Queue()
Qso = Queue.Queue()

Qci = Queue.Queue()
Qco = Queue.Queue()

receiveServer = threading.Thread(target= listener, args = (UDP_IP,UDP_PORTin,Qsi,))
crafterS = threading.Thread(target= packetcrafter, args = (Qsi,Qso,))
sendServer = threading.Thread(target= sender, args = (UDP_IP, UDP_PORTout,Qso,'S',))


receiveClient = threading.Thread(target= listener, args = (UDP_IP,UDP_PORTout,Qci,))
crafterC = threading.Thread(target= packetcrafter, args = (Qci,Qco,))
sendClient = threading.Thread(target= sender, args = (UDP_IP, UDP_PORTin,Qco,'C',))

sendServer.start()
receiveServer.start()
crafterS.start()

sendClient.start()
crafterC.start()
receiveClient.start()


# sender: creating socket that will send over Internet using UDP protocol
sender = socket.socket(socket.AF_INET, # Internet
                 socket.SOCK_DGRAM) # UDP

## We inject a packet to start message looping
# sender: creating socket that will send over Internet using UDP protocol
MESSAGE = "numero0" 
sender.sendto(MESSAGE, (UDP_IP, UDP_PORTout))



sendServer.join()
receiveServer.join()
sendClient.join()
receiveClient.join()

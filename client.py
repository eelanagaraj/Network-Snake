#!/usr/bin/python

""" client-side: listening for user inputs for snake,
		send user inputs as UDP packets to server,
		receives graphical rendering as UDP packets from server,
		renders graphics for user"""

import socket

# some UDP packet sending experiments yay!

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# note that data sent must be a string (double check, but can't send lists, etc. so will need to do some string parsing)
MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

# sender: creating socket that will send over Internet using UDP protocol
sender = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

# receiver: must bind to given listening address, will then listen for packets in loop later on
receiver = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
receiver.bind((UDP_IP, UDP_PORT))

# sender sends data as UDP packet
sender.sendto(MESSAGE, (UDP_IP, UDP_PORT))



while True:
    data, addr = receiver.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data
    sender.close()
    receiver.close()
    break

# initialize client socket

	# does socket need to have different ports for receiving vs listening???

# listen for user inputs (including no input)

# send user inputs to server socket in UDP packets

# receive UDP packets from server and render graphics for user
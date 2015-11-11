#!/usr/bin/python

""" client-side: listening for user inputs for snake,
		send user inputs as UDP packets to server,
		receives graphical rendering as UDP packets from server,
		renders graphics for user"""

import socket

# some UDP packet sending experiments yay!
My_IP = "10.251.54.255"
Sean_IP = "10.251.54.174"
UDP_IP = "10.251.48.230"
UDP_PORT = 4000

# note that data sent must be a string, though we can potentially use serializing libraries to send complex data objects
	# my fave serializable python module is cPickle (pretty fast, straightforward to use) so we can look into that if need be
MESSAGE = "Hey Sean!!!"

#print "UDP target IP:", UDP_IP
#print "UDP target port:", UDP_PORT
#print "message:", MESSAGE

# sender: creating socket that will send over Internet using UDP protocol
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# receiver: must bind to given listening address, will then listen for packets in loop later on
#receiver = socket.socket(socket.AF_INET, # Internet
                   # socket.SOCK_DGRAM) # UDP
#receiver.bind((My_IP, UDP_PORT))

#sender sends data as UDP packet
sender.sendto(MESSAGE, (Sean_IP, UDP_PORT))


"""
while True:
    data, addr = receiver.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data
    #sender.close()
    receiver.close()
    break
"""
# initialize client socket

	# does socket need to have different ports for receiving vs listening???

# listen for user inputs (including no input)

# send user inputs to server socket in UDP packets

# receive UDP packets from server and render graphics for user
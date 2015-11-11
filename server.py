#!/usr/bin/python

""" server-side: receive client's UDP packets of user inputs,
		perform game computations on these inputs,
		return entire graphical representation to client"""
import socket


UDP_IP = "10.251.48.230"
UDP_PORT = 5005

#receiver: must bind to given listening address, will then listen for packets in loop later on
receiver = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
receiver.bind((UDP_IP, UDP_PORT))



while True:
    data, addr = receiver.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data
    receiver.close()
    break





# initialize socket

# receive UDP packets on this socket

# extract user data from UDP packets instead of event-listening

# perform snake computations on this extracted data

# send UDP packet containing graphical rendering to the client socket
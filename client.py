#!/usr/bin/python

""" client-side: listening for user inputs for snake,
		send user inputs as UDP packets to server,
		receives graphical rendering as UDP packets from server,
		renders graphics for user"""

import socket

# some UDP packet sending experiments yay!

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock2 = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock2.bind((UDP_IP, UDP_PORT))

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))



while True:
    data, addr = sock2.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data
    sock.close()
    sock2.close()
    break

sock.close()
sock2.close()
# initialize client socket

	# does socket need to have different ports for receiving vs listening???

# listen for user inputs (including no input)

# send user inputs to server socket in UDP packets

# receive UDP packets from server and render graphics for user
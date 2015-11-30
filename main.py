#!/usr/bin/python
""" python network code yayayay """


import socket
import struct
import time


def function5():
	print 5

## Server master function listens for a time stamp, unpacks it waits delay 
## seconds after the timestamp and calls function funk
def ServerMeister(Server_ip = '10.251.51.211', Server_port = 5005, delay = 4, funk = function5):
	#TCP_IP = '127.0.0.1'
	TCP_IP = Server_ip
	TCP_PORT = Server_port
	BUFFER_SIZE = 20  # Normally 1024, but we want fast response

	packer = struct.Struct('d')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)

	conn, addr = s.accept()
	print 'Connection address:', addr
	while 1:
	    reftime = conn.recv(BUFFER_SIZE)
	    if not reftime: break
	    startref = packer.unpack(reftime)
	    conn.send('received')  # echo
	conn.close()
	#print startref[0]

	while (time.time() - delay)*1000 < startref[0]:	pass

	funk()

ServerMeister()

# try to actually get something to run on a remote server



# attempt to set up/start experimenting with network protocols, etc.

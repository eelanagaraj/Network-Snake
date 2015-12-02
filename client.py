#!/usr/bin/python

""" client-side: listening for user inputs for snake,
		send user inputs as UDP packets to server,
		receives graphical rendering as UDP packets from server,
		renders graphics for user"""

import ast
import pygame
import Queue
import random, sys
import socket
import struct
import time
import threading
from pygame.locals import * 

import helpers

Client_IP = "10.251.48.115"
Server_IP = "10.251.59.41"

def client(qi, ServerIP):
	sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	rate = 0.51
	## we start and customize the pygame gui
	pygame.init();
	s=pygame.display.set_mode((600, 600));
	pygame.display.set_caption('Snake');

	# initial snake block positions 
	xs = [290, 290, 290, 290, 290];
	ys = [290, 270, 250, 230, 210];


	# initial snake direction, score & position of the apple
	dirs = 0;
	score = 0;

	# we create our apple and our snake blocks
	block_size = (20, 20)
	appleimage = pygame.Surface((block_size[0], block_size[1]));
	# hacky bullsheeeet below so double check
	applepos = (330,270)
	appleimage.fill((0, 255, 0));
	img = pygame.Surface((block_size[0], block_size[1]));
	img.fill((255, 0, 0));

	# other stuff
	f = pygame.font.SysFont('Arial', 20);

	loops = 0
	curr_gui_number = 0
	dirs_list = [-1,-1,-1]
	pre1 = -1
	pre2 = -1
	sttime = time.time()
	while True:
		print 'iterating client'

		# we detect keystrokes and put them in our queue qo
		for e in pygame.event.get():
			if e.type == QUIT:
				sys.exit(0)
			elif e.type == KEYDOWN:
				if e.key == K_UP and dirs != 0:
					dirs = 2
				elif e.key == K_DOWN and dirs != 2:
					dirs = 0
				elif e.key == K_LEFT and dirs != 1:
					dirs = 3
				elif e.key == K_RIGHT and dirs != 3:
					dirs = 1

		pre1 = dirs_list[0]
		pre2 = dirs_list[1]

		dirs_list[0] = dirs
		dirs_list[1] = pre1
		dirs_list[2] = pre2

  		# send packet multiple times for redundancy
		packet = helpers.serializer(loops, dirs_list) 
		sender.sendto(packet, (ServerIP, 4001))
		sender.sendto(packet, (ServerIP, 4001))
		sender.sendto(packet, (ServerIP, 4001))

		# we wait and listen for incomming gui info in qi
		while time.time() - sttime - loops*rate < (rate - 0.1):		
			if qi.qsize() > 0:
				# need to unserialize packet
				seq_number,data = helper.unserializer(qi.get())

				# need to handle configuration sequence orderings here
				# should it just be < ??
				if (curr_gui_number <= seq_number) :
					curr_gui_number = seq_number
					guidict = ast.literal_eval(data)
					with qi.mutex:
						qi.queue.clear()
					if guidict['GameOver'] == True:
						sys.exit()
					xs = guidict['xs']
					ys = guidict['ys']  
					applepos = guidict['applepos']
					score = guidict['score']
					break

		##rendering when gui info received
		s.fill((255, 255, 255))
		s.blit(appleimage, applepos);
		for i in range(0, len(xs)):
			s.blit(img, (xs[i], ys[i]))
		
		t=f.render("score:" + str(score), True, (0, 0, 0));
		s.blit(t, (10, 10));
		pygame.display.update()
		
		while time.time() - sttime - loops*rate < (rate - 0.001):
			pass	
		loops += 1


## This Tcp wizardry sends timestamp to a server @ TCP_IP TCP_PORT waits delay seconds
## and then executes stuff, here this is print 5
def ClientConnectionHandler(ServerIP = Server_IP, ServerPort = 5005, delay = 4):

	TCP_IP = ServerIP
	TCP_PORT = ServerPort
	BUFFER_SIZE = 256

	packer = struct.Struct('d')
	reftime = packer.pack(time.time()*1000)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))

	# so here can we send the init position/config also
	# package it all up wiht reftime, etc., send as one tcp packet


	s.send(reftime)
	data = s.recv(BUFFER_SIZE)
	s.close()

	startref = packer.unpack(reftime)

	while (time.time() - delay)*1000 < startref[0]: pass

	Qci = Queue.Queue()
	
	ClientReciever = threading.Thread(target = helpers.listener, args = (Client_IP,4000,QCi))
	Client = threading.Thread(target = client, args = (Qci, ServerIP))
	
	ClientReciever.start()
	Client.start()
	
	ClientReciever.join()
	Client.join()

ClientConnectionHandler()
# some UDP packet sending experiments yay!
"""
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

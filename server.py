#!/usr/bin/python

""" server-side: receive client's UDP packets of user inputs,
		perform game computations on these inputs,
		return entire graphical representation to client"""

import ast
#import pygame
import Queue
import random, sys
import socket
import struct
import time
import threading
#from pygame.locals import *

import helpers

Client_IP = "10.251.48.115"
Server_IP = "10.251.59.41"

def server(qi, ClientIP):
	# function to detect collisions serpent->serpent & serpent->apple
	def collide(x1, x2, y1, y2, w1, w2, h1, h2):
		if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:
			return True
		else:
			return False
	    
	# stuff to do if you die
	def die(score):
		print 'Game Over, your score was: ' + str(score)
		return True
	def  nextstep(xs,ys,applepos,score,GameOver, dirs):
		i = len(xs)-1

		# if we bite ourselves -> death
		while i >= 3:
			if collide(xs[0], xs[i], ys[0], ys[i], block_size[0], block_size[1],block_size[0], block_size[1]):
				GameOver = die(score)
			i-= 1
		# if we hit an apple -> bigger snake + increment score
		if collide(xs[0], applepos[0], ys[0], applepos[1], 20, 10, 20, 10):
			score+=1;
			xs.append(700);
			ys.append(700);
			applepos = (random.randint(1, 29)*20-10, random.randint(1, 29)*20-10)
		# if we hit a wall -> death
		if xs[0] < 0 or xs[0] > 580 or ys[0] < 0 or ys[0] > 580: 
			GameOver = die(score)

		i = len(xs)-1

		# we update the position of the snake's body
		while i >= 1:
			xs[i] = xs[i-1];ys[i] = ys[i-1];i -= 1
		if dirs==0:
			ys[0] += 20
		elif dirs==1:
			xs[0] += 20
		elif dirs==2:
			ys[0] -= 20
		elif dirs==3:
			xs[0] -= 20
		return (xs,ys,applepos,score,GameOver)

	sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	rate = 0.051
	# initial snake block positions
	xs = [290, 290, 290, 290, 290]
	ys = [290, 270, 250, 230, 210]
		
	# initial snake direction, score & position of the apple
	dirs = 0;
	score = 0;
	#
	GameOver = False
	#\/ modification to see the snake eat the first apple
	applepos = (330,270)#(random.randint(0, 590), random.randint(0, 590));
	block_size = (20, 20)
	sttime = time.time()
	loops = 0
	while True:		
		# if we have a command in our queue
		while time.time() - sttime - loops*rate < (rate - 0.05):
			if qi.qsize() > 0:
				dirs = int(qi.get())
				break

		# here loops represents the config number we are sending back
		loops += 1
		gameinfo = nextstep(xs,ys,applepos,score,GameOver,dirs)
		xs = gameinfo[0]
		ys = gameinfo[1]
		applepos = gameinfo[2]
		score = gameinfo[3]
		GameOver = gameinfo[4]
		
		# we send gui info to the client
		guidict = dict()
		guidict['xs'] = xs
		guidict['ys'] = ys
		guidict['applepos'] = applepos
		guidict['score'] = score
		guidict['GameOver'] = GameOver
		packet = helpers.serializer(loops, guidict) 
		sender.sendto(packet, (ClientIP, 4001))
#		time.sleep(0.005)
		sender.sendto(packet, (ClientIP, 4001))
#		time.sleep(0.005)
		sender.sendto(packet, (ClientIP, 4001))

		if GameOver:
			print 'darn'
			sys.exit()


## Server master function listens for a time stamp, unpacks it waits delay 
## seconds after the timestamp and calls function funk
def ServerConnectionHandler(ServerIP = Server_IP, ServerPort = 5005, delay = 2):

	TCP_IP = ServerIP
	TCP_PORT = ServerPort
	BUFFER_SIZE = 20  # Normally 1024, but we want fast response

	packer = struct.Struct('d')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)

	conn, addr = s.accept()
	#print 'Connection address:', addr
	while 1:
	    reftime = conn.recv(BUFFER_SIZE)
	    if not reftime: break
	    startref = packer.unpack(reftime)
	    conn.send('received')
	conn.close()

	while (time.time() - delay)*1000 < startref[0]:	pass
	Qsi = Queue.Queue()

	ServerReciever = threading.Thread(target = helpers.server_listener, args = (ServerIP, 4000, Qsi))
	Server = threading.Thread(target = server, args = (Qsi, Client_IP))

	ServerReciever.start()
	Server.start()
	ServerReciever.join()
	Server.join()

ServerConnectionHandler()

"""
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

# send UDP packet containing graphical rendering to the client socket"""

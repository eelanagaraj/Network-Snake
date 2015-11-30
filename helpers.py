#!/usr/bin/python

""" helper functions, treat as header function to client and server """

import socket
import Queue
import threading
import time
import cPickle as pkl
import ujson

""" -assume data is of form: data = (seq_number, data_payload, prev_payloads)
	-payloads is a list of all data payloads that are included, 
		in decr sequence order (e.g. [recent, ..., oldest])
	-return tuple of: (new_current_seq, [most recent payload, ... oldest]) 
	**** maybe reverse within this function itself???? see what works best """
def packet_handler(curr_seq_number, seq_number, payloads) :
	# check if current sequence number matches the sent packet
	if (curr_seq_number == seq_number) :
		return (seq_number + 1, [payloads[0]]) 
	# if this packet is no longer useful 
	elif (curr_seq_number > seq_number) :
		return (curr_seq_number, [])
	# we're behind, return as many packets we have that are useful
	else :
		del payloads[seq_number - curr_seq_number + 1:]
		return (seq_number + 1, payloads)
		#OR if del is funky: return (seq_number + 1, payloads[:seq_number - curr_seq_number + 1])
		# see which is faster --> del may be better long run since modifies in place but idk 

""" function that puts data, sequence, etc. in serialized string form """	
def packer(seq_num, payloads) :
	# dictionary containing sequence number, list of packets, etc? 
	# test serialized objects with JSON vs cPickle??
	peanuts = {'seq_num': seq_num , 'payloads' : payloads}
	# cPickle --> NOTE not robust against malicious attacks
	return pkl.dumps(peanuts)
	# uJSON --> fast, C-backend, more robust to malicious attacks
	#return ujson.dumps(peanuts)
	

""" listen on port UDP_PORTin, at ip UDP_IP for udp packets 
	that we then push to our queue q """
def listener(UDP_IP, UDP_PORTin, q,):
	curr_seq = 0
	#receiver: must bind to given listening address, will then listen for packets in loop later on
	receiver = socket.socket(socket.AF_INET, # Internet
					 socket.SOCK_DGRAM) # UDP
	receiver.bind((UDP_IP, UDP_PORTin))
	# sender.bind((UDP_IP, UDP_PORTout))

	# we listen for packets and send them to the game thread/ put them in the queue
	while True:
		data, addr = receiver.recvfrom(512) # buffer size is 1024 bytes

		# this is where we wanna break down data & call packet handler
		# seq_num = ??? extract sequence number from data packet
		# payloads = ??? extract payloads from data packet
		(curr_seq, moves) = packet_handler(curr_seq, seq_num, payloads)
		#print data
		for move in reversed(moves) :
			q.put(move)
		#q.put(data)
		time.sleep(1)


""" listens to a queue q, pulls a packet if queue is not empty and
	sends it to FriendUDP_IP at port UDP_PORTout """
def sender(FriendUDP_IP, UDP_PORTout,q,b,):
	sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	while True:
		if q.qsize() > 0:#and count < 10:
			packet = q.get()
			sender.sendto(packet, (FriendUDP_IP, UDP_PORTout))
			print 'sent' + b + '\n'


""" bs testing function by sean """
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

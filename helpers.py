#!/usr/bin/python

""" helper functions, treat as header function to client and server """

import socket
import Queue
import threading
import time
import cPickle as pkl
#import ujson


""" Eela IP 10.251.51.241
	Matt IP 192.168.89.131
	Sean IP 10.251.48.115
"""

class Timer:
    def __init__(self, func=time.perf_counter):
        self.elapsed = 0.0
        self._func = func
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()



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


""" function that puts data, sequence, etc. in serialized string form 
	payloads should be a list of moves, most recent --> least """	
def serializer(seq_num, payloads) :
	peanuts = {'seq_num': seq_num , 'payloads' : payloads}
	# cPickle --> NOTE not robust against malicious attacks
	#return pkl.dumps(peanuts)
	# uJSON --> fast, C-backend, more robust to malicious attacks
	return ujson.dumps(peanuts)


""" un-serializes objects in the packet, returns (seq_num, payloads)"""
def unserializer(UDP_data) :
	# needs to be consistent with packer
	# cPickle
	#peanuts = pkl.loads(UDP_data)
	#return (peanuts['seq_num'], peanuts['payloads'])
	# ujson
	peanuts = ujson.loads(UDP_packet)
	return (peanuts['seq_num'], peanuts['payloads'])



""" listen on port UDP_PORTin, at ip UDP_IP for udp packets 
	that we then push to our queue q """
def listener(UDP_IP, UDP_PORTin, q,):
	curr_seq = 0
	#receiver: must bind to given listening address, will then listen for packets in loop later on
	receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	receiver.bind((UDP_IP, UDP_PORTin))
	
	# we listen for packets and send them to the game thread/ put them in the queue
	while True:
		data, addr = receiver.recvfrom(512) # buffer size is 1024 bytes
		q.put(data)


def server_listener(UDP_IP, UDP_PORTin, q,):
	curr_seq = 0
	#receiver: must bind to given listening address, will then listen for packets in loop later on
	receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	receiver.bind((UDP_IP, UDP_PORTin))
	
	# we listen for packets, but only queue moves that are relevant
	while True:
		data, addr = receiver.recvfrom(512) # buffer size is 1024 bytes
		seq_num, payloads = unserializer(data)
		(curr_seq, moves) = packet_handler(curr_seq, seq_num, payloads)
		# put moves on listening queue, oldest --> newest
		for move in reversed(moves) :
			q.put(move)


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

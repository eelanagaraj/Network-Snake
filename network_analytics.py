#!/usr/bin/python

import sys
import socket
import helpers
import time

""" use to test average rate of packet drops on network, etc."""



""" send_IP sends volume number of IP packets to receive_IP"""
def send_packets (volume, packet, receive_IP, port_num) :
	sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	for i in xrange(volume) :
		sender.sendto(packet, (receive_IP, port_num))

def count_received (expected_volume, match_data, receive_IP, receive_port):
	receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	receiver.bind((receive_IP, receive_port))
	packet_count = 0
	timeout = time.time() + 5
	print timeout
	while (packet_count < expected_volume and time.time() < timeout) :
		try : 
			data, addr = receiver.recvfrom(512)
			if data == match_data :
				packet_count += 1
				print packet_count
		except KeyboardInterrupt :
			print "packets received :", packet_count
			print "percent received :", packet_count/float(expected_volume)
			receiver.close()
			sys.exit()
	receiver.close()
	print "packets recceived :", packet_count
	print "percent received :", packet_count/float(expected_volume)

receiver_IP = "10.251.48.115"

packet = helpers.serializer(14, [1,0,3]) 
machine = int(raw_input("Sender machine press 0, receiver machine press 1"))
if machine :
	count_received(1000, packet, receiver_IP, 4001)
else :
	send_packets (1000, packet, receiver_IP, 4001)






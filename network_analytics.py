#!/usr/bin/python

import sys
import socket
import helpers

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
	while (packet_count < expected_volume) :
		try :
			data, addr = receiver.recvfrom(512)
			if data == match_data :
				packet_count = packet_count + 1
		except KeyboardInterrupt :
			print "packets received :", packet_count
			print "percent received :", packet_count/expected_volume
			sys.exit()
	print "packets recceived :", packet_count
	print "percent received :", packet_count/expected_volume

receiver_IP = "FILL IN"

packet = helpers.serializer(14, [1,0,3]) 
machine = raw_input("Sender machine press 0, receiver machine press 1")
if machine :
	count_received(1000, packet, receiver_IP, 4001)
else :
	send_packets (1000, packet, receiver_IP, 4001)






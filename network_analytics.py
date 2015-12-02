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
		gift = helpers.serializer(i, [1,3,5])
		sender.sendto(gift, (receive_IP, port_num))
		print "sent ", i
		time.sleep(0.005)

def count_received (expected_volume, match_data, receive_IP, receive_port):
	receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	receiver.bind((receive_IP, receive_port))
	packet_count = 0
	while (packet_count < expected_volume) :
		try : 
			data, addr = receiver.recvfrom(512)
			seq_num, moves = helpers.unserializer(data)
			#if data == match_data :
			packet_count += 1
			print 'count: ', packet_count, 'seq_num: ', seq_num
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






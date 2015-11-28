
##                                      (✪㉨✪) work in progress (✪㉨✪)
#                    /^\/^\
#                  _|__|  O|
#         \/     /~     \_/ \
#          \____|__________/  \
#                 \_______      \
#                         `\     \                 \
#                           |     |                  \
#                          /      /                    \
#                         /     /                       \\
#                       /      /                         \ \
#                      /     /                            \  \
#                    /     /             _----_            \   \
#                   /     /           _-~      ~-_         |   |
#                  (      (        _-~    _--_    ~-_     _/   |
#                   \      ~-____-~    _-~    ~-_    ~-_-~    /
#                     ~-_           _-~          ~-_       _-~   
#                        ~--______-~                ~-___-~


import pygame
import random, sys
import time
import threading
import Queue
import socket
import ast
from pygame.locals import *

def client(qi,qo):
	## GUI STUFF TO BE MOVED \/
	# we start and customize the pygame gui
	pygame.init();
	s=pygame.display.set_mode((600, 600));
	pygame.display.set_caption('Snake');

	# initial snake block positions 
	xs = [290, 290, 290, 290, 290];
	ys = [290, 270, 250, 230, 210];

	# number of frame per second the game can play at
	fps = 1

	# initial snake direction, score & position of the apple
	dirs = 0;
	score = 0;

	#\/ modification to see the snake eat the first apple
	applepos = (330,270)#(random.randint(0, 590), random.randint(0, 590));

	# we create our apple and our snake blocks
	block_size = (20, 20)
	appleimage = pygame.Surface((block_size[0], block_size[1]));
	appleimage.fill((0, 255, 0));
	img = pygame.Surface((block_size[0], block_size[1]));
	img.fill((255, 0, 0));

	# other stuff
	f = pygame.font.SysFont('Arial', 20);
	clock = pygame.time.Clock()


	while True:
		print 'iterating client'
		#dirs = 1
		for e in pygame.event.get():
			#print "<info>",e, "<info>"
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
			
			#print dirs
		qo.put(dirs)
		clock.tick(fps)
		if qi.qsize() > 0:
			guidict = ast.literal_eval(qi.get())
			with qi.mutex:
				qi.queue.clear()
			if guidict['GameOver'] == True:
				sys.exit()
			xs = guidict['xs']
			ys = guidict['ys']  
			applepos = guidict['applepos']
			score = guidict['score']
		else:
			pass
		## weird bottom stuff
		s.fill((255, 255, 255))
		##rendering bit when packet received
		for i in range(0, len(xs)):
			s.blit(img, (xs[i], ys[i]))
			# apple
			s.blit(appleimage, applepos);
			# score
			t=f.render("score:" + str(score), True, (0, 0, 0));
			s.blit(t, (10, 10));
			pygame.display.update()


def server(qi,qo):
	# function to detect collisions serpent->serpent & serpent->apple
	def collide(x1, x2, y1, y2, w1, w2, h1, h2):
		if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:
	        #f=pygame.font.SysFont('Arial', 30);
	        #t=f.render('collision', True, (0, 0, 0));
	        #screen.blit(t, (10, 270));
	        #pygame.display.update();
	        #pygame.time.wait(200);
			return True
		else:
			return False
	    
	    
	# stuff to do if you die
	def die(score):
		print 'Game Over, your score was: ' + str(score)
	    #f=pygame.font.SysFont('Arial', 30);
	    #t=f.render('Your score was: '+str(score), True, (0, 0, 0));
	    #screen.blit(t, (10, 270));
	    #pygame.display.update();
	    #pygame.time.wait(2000);
		return True

	print 'game started'
	# initial snake block positions
	xs = [290, 290, 290, 290, 290]
	ys = [290, 270, 250, 230, 210]
	# number of frame per second the game can play at
	fps = 1
	# initial snake direction, score & position of the apple
	dirs = 0;
	score = 0;
	#
	GameOver = False
	#\/ modification to see the snake eat the first apple
	applepos = (330,270)#(random.randint(0, 590), random.randint(0, 590));
	block_size = (20, 20)
	while True:
		# we run at one fps
		### clock.tick(fps)
		
		## Following lines will be server side stuff
		# if we have a command in our queue
		if qi.qsize() > 0:
			dirs = int(qi.get())
			print dirs, "direction", type(dirs)
		else:
			pass
		# REF 1*

		# weird coding from the misterious original writer of this thing
		i = len(xs)-1

		# if we bite ourselves -> death
		while i >= 2:
			if collide(xs[0], xs[i], ys[0], ys[i], block_size[0], block_size[1],block_size[0], block_size[1]):
				GameOver = die( score)
			i-= 1
		# if we hit an apple -> bigger snake + increment score
		if collide(xs[0], applepos[0], ys[0], applepos[1], 20, 10, 20, 10):
			score+=1;
			xs.append(700);
			ys.append(700);
			applepos=(random.randint(0,590),random.randint(0,590))

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
		# we send gui info to the client
		print 'iterating server'
		guidict = dict()
		guidict['xs'] = xs
		guidict['ys'] = ys
		guidict['applepos'] = applepos
		guidict['score'] = score
		guidict['GameOver'] = GameOver
		out = str(guidict)
		qo.put(out)
		if GameOver:
			print 'darn'
			sys.exit()
		time.sleep(1)

Q1 = Queue.Queue()
Q2 = Queue.Queue()
gui = threading.Thread(target= client, args = (Q1,Q2,))
server = threading.Thread(target= server, args = (Q2,Q1,))
gui.start()
server.start()
gui.join()
server.join()

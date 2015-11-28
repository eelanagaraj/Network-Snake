### the old version of the game just for reference

import pygame
import random, sys
import time
import threading
import Queue
import socket
from pygame.locals import *


# function to detect collisions serpent->serpent & serpent->apple
def collide(screen, x1, x2, y1, y2, w1, w2, h1, h2):
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
def die(screen, score):
    f=pygame.font.SysFont('Arial', 30);
    t=f.render('Your score was: '+str(score), True, (0, 0, 0));
    screen.blit(t, (10, 270));
    pygame.display.update();
    pygame.time.wait(2000);
    sys.exit(0)
    
def play(Q, fps):
    print 'game started'
    # server side gui stuff here need to share it with client
    
    # \/ initial snake block positions \/
    xs = [290, 290, 290, 290, 290];
    ys = [290, 270, 250, 230, 210];
    
    # number of frame per second the game can play at
    #FPS = 1
    
    # \/ initial snake direction, score & position of the apple
    dirs = 0;
    score = 0;
    
    #\/ modification to see the snake eat the first apple
    applepos = (330,270)#(random.randint(0, 590), random.randint(0, 590));
    
    # we start and customize the pygame gui
    pygame.init();
    s=pygame.display.set_mode((600, 600));
    pygame.display.set_caption('Snake');
    
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
        # we run at one fps
        clock.tick(fps)
        
        ## Following lines will be server side stuff
        # if we have a command in our queue
        if Q.qsize() > 0:
            dirs = Q.get()
        else:
            pass
        # REF 1*
        i = len(xs)-1
        
        while i >= 2:
            if collide(s, xs[0], xs[i], ys[0], ys[i], block_size[0], block_size[1],block_size[0], block_size[1]):
                die(s, score)
            i-= 1
            
    
        if collide(s, xs[0], applepos[0], ys[0], applepos[1], 20, 10, 20, 10):
            score+=1;
            xs.append(700);
            ys.append(700);
            applepos=(random.randint(0,590),random.randint(0,590))
        
        # if we hit a wall -> death
        if xs[0] < 0 or xs[0] > 580 or ys[0] < 0 or ys[0] > 580: 
            die(s, score)
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
        s.fill((255, 255, 255))    
        ## need to take all this gui info -> pickle it 
        ## stick it in a queue to have it sent to the client
        
        ## client side stuff: blit the snake, the apple & score
        #snake
        for i in range(0, len(xs)):
            s.blit(img, (xs[i], ys[i]))
        # apple
        s.blit(appleimage, applepos);
        # score
        t=f.render("score:" + str(score), True, (0, 0, 0));
        s.blit(t, (10, 10));
        pygame.display.update()
                    
def client(fps):
    UDP_IP =  "127.0.0.1"
    UDP_PORT = 4000
    # sender: creating socket that will send over Internet using UDP protocol
    sender = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    v = ('1','2','1','2','1','2','1','2','3','2','3','2','3','4','3')
    ## need to put pygame instance in here
    # one hand will receive UIinputs 
    # other will receive packets from server and diplay in gui
    for i in range(1,13):
        MESSAGE = v[i - 1]
        time.sleep(1)
        sender.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        print 'message sent'+' ' +MESSAGE
        
def server(fps):
    ## our server thread 
    
    # we setup our ports
    UDP_IP = "127.0.0.1"
    UDP_PORT = 4000
    #receiver: must bind to given listening address, will then listen for packets in loop later on
    receiver = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    receiver.bind((UDP_IP, UDP_PORT))
    
    # we create a queue and start our game thread
    q = Queue.Queue()
    game = threading.Thread(target= play, args=(q,fps,))
    game.start()
    
    # we listen for packets and send them to the game thread
    while True:
        data, addr = receiver.recvfrom(512) # buffer size is 1024 bytes
        q.put(int(data))
        
    
def master():
    # we define up here the game rate
    FPS = 1
    send = threading.Thread(target= client, args = (FPS,))
    receive = threading.Thread(target= server, args = (FPS,))
    send.start()
    receive.start()
    send.join()
    receive.join()
#REF 1
    #dirs = 1
        #for e in pygame.event.get():
        #    print "<info>",e, "<info>"
        #    if e.type == QUIT:
        #        sys.exit(0)
        #    elif e.type == KEYDOWN:
        #        if e.key == K_UP and dirs != 0:
        #            dirs = 2
        #        elif e.key == K_DOWN and dirs != 2:
        #            dirs = 0
        #        elif e.key == K_LEFT and dirs != 1:
        #            dirs = 3
        #        elif e.key == K_RIGHT and dirs != 3:
        #            dirs = 1

-----------------------------------------------------------------------------------------------------------------------------
### /\ STUFF ABOVE KEPT FOR REFERENCE /\

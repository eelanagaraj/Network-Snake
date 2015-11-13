import time

    ## This thing will be running in the server will play the game using
    ## inputs from master network side of thing to whom it will return 
    ## gui data to be sent for the client

def ServerSlave(Qi,Qo):
    origin = time.time()*1000 
    FPS = 1
    speed = 1000/FPS
    counter = 0
    current_sequence = 0
    while True:
    # if input queue Qi non empty pull user inputs
    	
    	# run calc w/ or w/out user input 
    # cumulative ack system to handle dropped UDP packets:

    # pop next UDP packet off queue
    # pass in the packet to packet_handler:

    # (new_curr, payloads) = packet_handler(current_sequence, ..., ..., ...)
    # current_sequence = new_curr
    # for p in reversed(payloads) :
        # run computations sequentially, queue to send to client

	
    	# put gui data in queue Qo to be sent by network thread
        while (time.time()*1000 - origin - counter*speed) < speed:
            pass
            counter += 1


    """ assume data is of form: data = (seq_number, prev_included, data_payload, prev_payloads)
        payloads is a list of all data payloads that are included, in decr sequence order (e.g. [recent, ..., oldest])
        return tuple of: (new_current_seq, [most recent payload, ... oldest]) 
        **** maybe reverse within this function itself???? see what works best """
def packet_handler(curr_seq_number, seq_number, number_payloads, payloads) :
    # check if current sequence number matches the sent packet
    if (curr_seq_number == seq_number) :
        return (seq_number + 1, [payloads[0]]) 
    # if this packet is no longer useful 
    elif (curr_seq_number > seq_number) :
        return (curr_seq_number, [])
    # we're behind, return as many packets we have 
    else :
        del payloads[seq_number - curr_seq_number + 1:]
        return (seq_number + 1, payloads)
        #OR if del is funky: return (seq_number + 1, payloads[:seq_number - curr_seq_number + 1])
        # see which is faster --> del may be better long run since modifies in place but idk
        
        
        
    #### STUFF TO BE transplanted to this function for the game to play, not complete yet just putting it up here so you know
    #### what im up to
    
    """"# function to detect collisions serpent->serpent & serpent->apple
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

	print 'game started'
    # server side gui stuff here need to share it with client
    
    # \/ initial snake block positions \/
    xs = [290, 290, 290, 290, 290];
    ys = [290, 270, 250, 230, 210];
    
    # number of frame per second the game can play at
    fps = 1
    
    # \/ initial snake direction, score & position of the apple
    dirs = 0;
    score = 0;
    
    #\/ modification to see the snake eat the first apple
    applepos = (330,270)#(random.randint(0, 590), random.randint(0, 590));
    

    ## GUI STUFF TO BE MOVED \/
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
    ## /\ /\ /\ /\
    
    # other stuff
    f = pygame.font.SysFont('Arial', 20);
    clock = pygame.time.Clock()
    
    while True:
        # we run at one fps
        clock.tick(fps)
        
        ## Following lines will be server side stuff
        # if we have a command in our queue
        if qi.qsize() > 0:
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

       	guidict = dict()
       	guidict['xs'] = xs
        guidict['ys'] = ys
        guidict['applepos'] = applepos
        guidict['score'] = score

	packet = str(guidict)
	## push packet to qo
	
	
        ## client side stuff: blit the snake, the apple & score
        #snake
        for i in range(0, len(xs)):
            s.blit(img, (xs[i], ys[i]))
        # apple
        s.blit(appleimage, applepos);
        # score
        t=f.render("score:" + str(score), True, (0, 0, 0));
        s.blit(t, (10, 10));
        pygame.display.update()"""




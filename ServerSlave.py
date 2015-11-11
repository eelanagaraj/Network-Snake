import time

## This thing will be running in the server will play the game using
## inputs from master network side of thing to whom it will return 
## gui data to be sent for the client
def ServerSlave(Qi,Qo):
  origin = time.time()*1000 
  FPS = 1
  speed = 1000/FPS
  counter = 0
  while True:
  	# if input queue Qi non empty pull user inputs
  	
  	# run calc w/ or w/out user input 
  	
  	# put gui data in queue Qo to be sent by network thread
  	while (time.time()*1000 - origin - counter*speed) < speed:
  		pass
  	counter += 1

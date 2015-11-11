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




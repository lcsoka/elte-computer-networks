import socket
import struct
import math
import random
import time 

packer = struct.Struct('1s I')

def tryLower(number):
    msg = (b'<',number)
    tryNumber(msg)

def tryHigher(number):
    msg = (b'>',number)
    tryNumber(msg)

def tryExact(number):
    msg = (b'=',number)
    tryNumber(msg)

def tryNumber(msg):
    msg_packed = packer.pack(*msg)

    sock.sendall(msg_packed)
    # msg_packed = sock.recv(8)
    # response = packer.unpack(msg_packed)
    # handleResponse(msg,response)
    
def handleResponse(msgSent, response):
    print(msgSent[0])
    print(response[0])

    if response[0] == b'V':
        return

    # tried lower
    if msgSent[0] == b'<':

        if response[0] == b'I':
            maxBound = msgSent[1]
        else:
            tryHigher(msgSent[1])
            return
    # tried higher
    elif msgSent[0] == b'>':
        if response[0] == b'I':
            minBound = msgSent[1]
        else:
            tryLower(msgSent[1])
            return
    #tried exact
    elif msgSent[0] == b'=':
        return

    tryHigher(math.floor((minBound+maxBound)/2))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("127.0.0.1", 5555))
    minBound = 0
    maxBound = 100
    numberFound = False
    comparators = [b"<",b">"]

    while not numberFound:
        guess = random.randint(minBound, maxBound + 1)

        if (guess == minBound or guess == maxBound or maxBound - minBound <= 1):
            comparison = b'='
        else:
            comparison = random.choice(comparators)
        
        guessMessage = (comparison,guess)
        print(guessMessage)
        guessPacked = packer.pack(*guessMessage)
        sock.sendall(guessPacked)

        responsePacked = sock.recv(8)
        msg = packer.unpack(responsePacked)
        response = msg[0]
        
        if(response == b'I'):
            if (comparison == b"<"):
                maxBound = guess - 1
            elif (comparison == b">"):
                minBound = guess + 1
            elif (comparison == b"="):
                minBound == guess
                maxBound == guess
        elif (response == b'N'):
            if(comparison == b'<'):
                minBound = guess
            elif (comparison == b'>'):
                maxBound = guess
        elif (response == b'Y'):
            print("WIN!")
            numberFound = True
        elif (response == b'K' or response == b'V'):
            print("LOST!")
            numberFound = True
        time.sleep(1)
    sock.close()
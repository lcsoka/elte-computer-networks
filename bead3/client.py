import socket
import struct
import math
import random
import time 
import sys

packer = struct.Struct('1s I')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((sys.argv[1], int(sys.argv[2])))
    minBound = 0
    maxBound = 100
    numberFound = False
    comparators = [b"<",b">"]

    while not numberFound:
        guess = random.randint(minBound, maxBound)
        print("minBound: {0}, maxBound: {1}, guess: {2}".format(minBound,maxBound, guess))
        if (maxBound - minBound <= 1):
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
            break
        elif (response == b'K' or response == b'V'):
            print("LOST!")
            numberFound = True
            break
        sleepTime = random.randint(1, 2)
        print("Waiting {0}s...".format(sleepTime))
        time.sleep(sleepTime)
    sock.close()
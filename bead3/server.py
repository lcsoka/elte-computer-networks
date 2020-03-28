import socket
import json
import random
import struct
import time 
import select

randomNumber = random.randint(0,100)
socks = []
packer = struct.Struct('1s I')

print("Random number: " + str(randomNumber))

def processMessage(msg, client):
    operator = msg[0]
    number = msg[1]

    responseList = ['',0]

    if(operator == b"<"):
        if(randomNumber < number):
            responseList[0] = b'I'
        else:
            responseList[0] = b'N'
    elif(operator == b">"):
        if(randomNumber > number):
            responseList[0] = b'I'
        else:
            responseList[0] = b'N'
    elif(operator == b"="):
        if(randomNumber == number):
            responseList[0] = b'Y'
        else:
            responseList[0] = b'N'
    else:
        ## Hibas keres
        ## Bontsuk a kapcsolatot
        socks.remove(client)
        client.close()
        return
    
    response = tuple(responseList)
    msg_packed = packer.pack(*response)
    client.send(msg_packed)

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", 5555))
srv.listen()
socks.append(srv)

while True:
    readable, writeable, err = select.select(socks, [], [], 0)

    for s in readable:
        if s == srv:
            client, client_address = srv.accept()
            print("New client from: {} address".format(client_address))
            socks.append(client)
        else:
            msg_packed = s.recv(8)
            # Uzenetet kaptunk
            if msg_packed: 
                msg = packer.unpack(msg_packed)
                if msg:
                    # Sikerult kicsomagolni az uzenetet
                    for sock in socks:
                        if sock == s and sock != srv:
                            # Megtalaltuk a klienst, feldolgozzuk az uznetet es visszakuldjuk a valaszt
                            processMessage(msg, sock)
                            time.sleep(1)
            else:
                # Nincs uzenet, bontjuk a kapcsolatot, es toroljuk a socketet
                print("Client disconnected")
                socks.remove(s)
                s.close()
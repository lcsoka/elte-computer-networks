import socket
import sys
import select
import zlib
import time 
from datetime import datetime, timedelta

ip = sys.argv[1]
port = int(sys.argv[2])
socks = []

db = dict()

# listen for incoming connections
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((ip, port))
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
            msg = s.recv(1024)
            if(msg):
                decoded = msg.decode('UTF-8')
                data = decoded.split('|')
                if(len(data) == 2 or len(data) == 5 ):
                    dir = data[0]
                    if dir == 'BE':
                        # store
                        file_id = data[1]
                        valid_time = datetime.timestamp(datetime.now() + timedelta(seconds=int(data[2])))
                        crc_length = data[3]
                        crc	= data[4]

                        # store in db
                        db[file_id] = [crc,crc_length,valid_time]
                        # print(db)
                        s.send('OK'.encode('UTF-8'))
                    elif dir == 'KI':
                        # get
                        file_id = str(int(data[1]))
                        result = db[file_id]
                        if result:
                            # check validity
                            now = datetime.timestamp(datetime.now())
                            if result[2] >= now:
                                s.send('{}|{}'.format(result[1],result[0]).encode('UTF-8'))
                                # s.send((str(result[1])+'|'+str(result[0])).encode('UTF-8'))
                                s.close()
                                socks.remove(s)
                            else:
                                s.send(b'0|')
                                s.close()
                                socks.remove(s)
                                print('not valid')

                                # delete from dict
                                del db[file_id]

                        else:
                            s.send(b'0|')
                            s.close()
                            socks.remove(s)
                    else:
                        print('Invalid message.')    
                else:
                    print('Invalid message.')
            else:
                print("Client disconnected")
                socks.remove(s)
                s.close()
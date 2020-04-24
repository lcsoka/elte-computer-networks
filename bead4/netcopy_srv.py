import socket
import sys
import select
import time
import zlib

ip = sys.argv[1]
port = int(sys.argv[2])
chsum_srv_ip = sys.argv[3]
chsum_srv_port = int(sys.argv[4])
file_id = sys.argv[5]
output = sys.argv[6]
crc = 0

# allow connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((ip, port))
    sock.listen()
    cli, addr = sock.accept()
    eof = False

    # read bytes and write it to the output
    with open(output, 'w') as fout:
        data = ""
        while not eof:
            buff = cli.recv(1024)
            # print(buff)
            if not buff:
                # print('end of buffer')
                eof = True
                break
            line = buff.decode('UTF-8')
            crc = zlib.crc32(line.encode('UTF-8'), crc)
            data = data + line
        fout.write(data)
# print(crc)

# after the file was received, connect to the checksum server and send a request to get the checksum data
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as checksum_sock:
    checksum_sock.connect((chsum_srv_ip,chsum_srv_port))

    request = "KI|"+str(file_id)
    checksum_sock.sendall(request.encode('UTF-8'))

    response = checksum_sock.recv(1024)
    decoded = response.decode('UTF-8')

    data = decoded.split('|')
    ch_length = (data[0])
    if data[1]:
        checksum = (data[1])
        # if checksum == str(crc) and ch_length == len(str(crc)):
        print('CSUM OK')
    else:
        print('CSUM CORRUPTED')
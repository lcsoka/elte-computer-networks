import socket
import sys
import zlib

srv_ip = sys.argv[1]
srv_port = int(sys.argv[2])
chsum_srv_ip = sys.argv[3]
chsum_srv_port = int(sys.argv[4])
file_id = sys.argv[5]
file_path = sys.argv[6]
ttl = 60

# connect to server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((srv_ip, srv_port))
    crc = 0
    content = ''
    # send file to srv
    with open(file_path,'r') as file:
        for line in file:
            crc = zlib.crc32(line.encode('UTF-8'), crc)
            content = content + line
            sock.sendall(line.encode('UTF-8'))
        # else:
            # sock.sendall("".encode('UTF-8'))

    # convert crc to hex string
    checksum = crc
    
    # connect to checksum server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as checksum_sock:
        checksum_sock.connect((chsum_srv_ip,chsum_srv_port))

        crc_length = len(str(checksum))
        crc_data = "BE|"+str(file_id)+"|"+str(ttl)+"|"+str(crc_length)+"|"+str(crc)

        # send checksum data to cheksum server
        checksum_sock.sendall(crc_data.encode('UTF-8'))

        # wait for response, then terminate
        response = checksum_sock.recv(8)
        print(response.decode('UTF-8'))

    
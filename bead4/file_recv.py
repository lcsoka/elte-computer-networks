import socket
import hashlib
import zlib

crc = 0
md5 = hashlib.md5()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(('127.0.0.1', 5555))
    sock.listen()
    cli, addr = sock.accept()

    with open('output.bin', 'wb') as fout:
        while True:
            buff = cli.recv(1024)
            if not buff:
                break

            fout.write(buff)

            crc = zlib.crc32(buff, crc)
            md5.update(buff)

    print("CRC32: ", hex(crc))
    print("MD5: ", md5.hexdigest())

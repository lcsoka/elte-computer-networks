import socket
import hashlib
import zlib

crc = 0
md5 = hashlib.md5()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('127.0.0.1', 5555))
    with open('data.bin', 'rb') as fin:
        while True:
            buff = fin.read(1024)
            if not buff:
                break
            crc = zlib.crc32(buff, crc)
            md5.update(buff)

            sock.send(buff)

    print("CRC32: ", hex(crc))
    print("MD5: ", md5.hexdigest())


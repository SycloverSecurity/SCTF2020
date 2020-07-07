
import socket
import sys
import os
import itertools
import string
from hashlib import sha256

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

#host = socket.gethostname() 
host = '47.108.71.166'
#host = '47.251.35.157'
port = 23333

s.connect((host, port))



# url_ = "https://www.google.com".encode('utf-8')
# s.send(url_)

def send_zip(server:socket.socket):
    zipfile = r'F:\Documents\Syclover\SCTF2020\EasyMojo\Exp\stage1.zip'
    zipfile_size = os.path.getsize(zipfile)
    server.send(f"{zipfile_size}".encode('utf-8'))
    msg = server.recv(1024)
    print(msg.decode('utf-8'), end='')
    with open(zipfile, 'rb') as f:
        while True:
            data = f.read(1024)
            if len(data) > 0:
                server.send(data)
            else:
                break
    print('sending complete')

def recv_show(server:socket.socket):
    msg = server.recv(1024).decode('utf-8')
    print(msg, end='')

def POW(sample_hash):
    for c in itertools.product(string.printable[0:36], repeat=5):
        sample = f"SCTF{''.join(c)}"
        if sha256(sample.encode('utf-8')).hexdigest() == sample_hash:
            return sample

# while True:
#     msg = s.recv(1024)
#     print(msg.decode('utf-8'), end='')
#     content = input()
#     if content == 'sendzip':
#         send_zip(s)
#     else:
#         s.send(content.encode('utf-8'))

if __name__=='__main__':
    recv_show(s)
    hash_ = s.recv(1024).decode('utf-8').split(':')[1].split('\n')[0].strip()
    print(f"hash: [{hash_}]")
    sample = POW(hash_)
    print(f"sample: [{sample}]")
    s.send(sample.encode('utf-8'))
    while True:
        msg = s.recv(1024)
        print(msg.decode('utf-8'), end='')
        content = input()
        if content == 'sendzip':
            send_zip(s)
        else:
            s.send(content.encode('utf-8'))
    
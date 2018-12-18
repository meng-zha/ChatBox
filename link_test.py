from socket import *
from time import ctime

HOST = '166.111.140.14'
PORT = 8000
BUFSIZ = 1024
ADDR = (HOST, PORT)

c = socket(AF_INET, SOCK_STREAM)
c.connect(ADDR)

while True:
    data = input('>')
    if not data:
        break
    c.send(data.encode())
    data = c.recv(BUFSIZ)
    if not data:
        break
    print(data.decode('utf-8'))

c.close()
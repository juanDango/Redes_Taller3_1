#!/usr/bin/env python3

import socket

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
with open('recibido.txt', 'wb') as f:
    print('Se ha abierto el archivo')
    while True:
        print('Recibiendo los datos...')
        data = s.recv(BUFFER_SIZE)
        print('data=', repr(data))
        if not data:
            f.close()
            print ('Archivo cerrado')
            break
        # write data to a file
        f.write(data)

print('Successfully get the file')
s.close()
print('Connection closed')


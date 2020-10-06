#!/usr/bin/env python3

import socket

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024
BEG_RECV = 'BEG_RECV'
OK = 'OK'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((TCP_IP, TCP_PORT))
    print('Se ha establecido una conexion exitosa con el servidor.')
except:
    print('No se ha podido establecer una conexion con el servidor.')
    exit()


#Se envia un mensaje inicial al servidor
mensajeInicial = b'Hola, querido servidor'
s.send((mensajeInicial))
print('Se ha enviado el mensaje inicial: ', repr(mensajeInicial))

with open('recibido.txt', 'wb') as f:
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

print('Se ha recibido el archivo de manera exitosa.')
s.close()
print('Conexion cerrada.')


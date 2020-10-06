#!/usr/bin/env python3

import socket

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024
BEG_RECV = b'BEG_RECV'
OK = b'OK'
FILE_OPTS = b'FILE_OPTS'
FILENAMES_SENT = b'FILENAMES_SENT'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((TCP_IP, TCP_PORT))
    print('Se ha establecido una conexion exitosa con el servidor.')
except:
    print('No se ha podido establecer una conexion con el servidor.')
    exit()


#Se envia un mensaje inicial al servidor
mensajeInicial = BEG_RECV
s.send((mensajeInicial))
print('Enviando comando: ', repr(mensajeInicial))
print('El cliente esta listo para recibir archivos.')

mensajeConfirmacion = s.recv(BUFFER_SIZE)
if(repr(mensajeConfirmacion) != repr(OK)):
    print(repr(mensajeConfirmacion))
    print('No se ha recibido el mensaje %s esperado, finalizando conexion' %(repr(OK)))
    exit()  
print('Comando recibido: ', repr(mensajeConfirmacion))

mensajeOpcionesArchivos = s.recv(BUFFER_SIZE)
if(repr(mensajeOpcionesArchivos) != repr(FILE_OPTS)):
    print(repr(mensajeOpcionesArchivos))
    print('No se ha recibido el mensaje %s esperado, finalizando conexion' %(repr(FILE_OPTS)))
    exit()  
print('Comando recibido: ', repr(mensajeOpcionesArchivos))

print('Escoja el numero de archivo a enviar')
mensajeNombreArchivo = s.recv(BUFFER_SIZE)
numArchivo = 1
while (mensajeNombreArchivo != FILENAMES_SENT):
    print(str(numArchivo) + '. ' + repr(mensajeNombreArchivo) + '\n')  
    mensajeNombreArchivo = s.recv(BUFFER_SIZE)
    numArchivo+=1

"""
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
"""

#!/usr/bin/env python3

import socket
import struct
import datetime

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024
BEG_RECV = b'BEG_RECV'
OK = b'OK'
FILE_OPTS = b'FILE_OPTS'
FILENAMES_SENT = b'FILENAMES_SENT'
ERR = b'ERR'
END_TRANSMISSION = b'END_TRANSMISSION'

def sendOneMessage(socket, data):
    length = len(data)
    socket.sendall(struct.pack('!I', length))
    socket.sendall(data)

def receiveAll(socket, count):
    buf = b''
    while count:
        newbuf = socket.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def receiveOneMessage(socket):
    #El length esta empacado en exactamente 4 bytes.
    lengthBuf = receiveAll(socket, 4)
    length, = struct.unpack('!I', lengthBuf)
    return receiveAll(socket, length)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((TCP_IP, TCP_PORT))
    print('Se ha establecido una conexion exitosa con el servidor.')
except:
    print('No se ha podido establecer una conexion con el servidor.')
    s.close()
    exit()

#Se envia un mensaje inicial al servidor
sendOneMessage(s, BEG_RECV)
print('Enviando comando: ', repr(BEG_RECV))
print('El cliente esta listo para recibir archivos.')

mensajeConfirmacion = receiveOneMessage(s)
if(repr(mensajeConfirmacion) != repr(OK)):
    print(repr(mensajeConfirmacion))
    print('No se ha recibido el mensaje %s esperado, finalizando conexion' %(repr(OK)))
    err = receiveOneMessage(s)
    print('Comando recibido: ', repr(err))
    s.close()
    exit()  
print('Comando recibido: ', repr(mensajeConfirmacion))

mensajeOpcionesArchivos = receiveOneMessage(s)
if(repr(mensajeOpcionesArchivos) != repr(FILE_OPTS)):
    print(repr(mensajeOpcionesArchivos))
    print('No se ha recibido el mensaje %s esperado, finalizando conexion' %(repr(FILE_OPTS)))
    err = receiveOneMessage(s)
    print('Comando recibido: ', repr(err))
    s.close()
    exit()  
print('Comando recibido: ', repr(mensajeOpcionesArchivos))

print('Los archivos disponibles en el servidor son: ')
mensajeNombreArchivo = receiveOneMessage(s)
numArchivo = 1
files = []
while (mensajeNombreArchivo != FILENAMES_SENT):
    ruta = repr(mensajeNombreArchivo)
    archivo = ruta[ruta.find("'")+1:-1]
    files.append(archivo)
    print(str(numArchivo) + '. ' + archivo)  
    mensajeNombreArchivo = receiveOneMessage(s)
    numArchivo+=1
print('Comando recibido: ', repr(mensajeNombreArchivo))
#Se resta 1 porque vamos a la posicion del arreglo en que se encuentra el archivo en el servidor
try:
    archivoElegido = int(input('Escoja el numero de archivo a recibir: \n')) - 1
    sendOneMessage(s, str(archivoElegido).encode())
except:
    print('Opcion incorrecta. Cerrando comunicacion con el servidor.')
    s.close()
    exit()

confirmacionArchivoElegido = receiveOneMessage(s)
if(repr(confirmacionArchivoElegido) != repr(OK)):
    print('Comando recibido: ', repr(confirmacionArchivoElegido))
    print('Error. Cerrando la conexion con el servidor.')
    s.close()
    exit()

print('Comando recibido: ', repr(confirmacionArchivoElegido))
print('El servidor ha verificado el nombre del archivo.')
print('Comenzando transferencia de datos...')

with open(files[archivoElegido], 'wb') as f:
    while True:
        data = receiveOneMessage(s)
        print('data = ' + repr(data) + '\n\n')
        if repr(data) == repr(END_TRANSMISSION):
            fechaFinTransmision = datetime.datetime.now()
            print('Fecha fin transmision archivo: ', fechaFinTransmision)
            f.close()
            print('Comando recibido: ', repr(END_TRANSMISSION))
            print('Archivo cerrado')
            break
        f.write(data)


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

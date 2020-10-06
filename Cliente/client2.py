#!/usr/bin/env python3

import socket
import struct
import datetime
import hashlib
import os
from hmac import compare_digest
import sys

TCP_PORT = 9001
BUFFER_SIZE = 1024
BEG_RECV = b'BEG_RECV'
OK = b'OK'
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
    TCP_IP = socket.gethostname()
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

print('Comenzando transferencia de datos...')
digestGenerado = hashlib.md5()
recibido = repr(receiveOneMessage(s))[2:-1]
archivoElegido = recibido[recibido.rfind('/')+1:]
numPaquetesRecibidos = 0
bytesRecibidos = 0
with open(archivoElegido, 'wb') as f:
    while True:
        data = receiveOneMessage(s)
        if repr(data) == repr(END_TRANSMISSION):
            fechaFinTransmision = str(datetime.datetime.now())
            sendOneMessage(s, fechaFinTransmision.encode())
            print('Fecha fin transmision archivo: ', fechaFinTransmision)
            f.close()
            print('Comando recibido: ', repr(END_TRANSMISSION))
            print('Se ha terminado de escribir el archivo ' + archivoElegido)
            break
        print('data = ' + repr(data) + '\n\n')
        f.write(data)
        digestGenerado.update(data)
        print(data)
        numPaquetesRecibidos += 1
        bytesRecibidos += sys.getsizeof(data)

digestG = digestGenerado.hexdigest().encode()
digestRecibido = receiveOneMessage(s)

if not compare_digest(digestG, digestRecibido):
    sendOneMessage(s, ERR)
    os.remove(archivoElegido)
    print('Comando enviado: ', repr(ERR))
    print('La integridad del archivo no pudo ser verificada. Finalizando conexion.')
    s.close()
    exit()
sendOneMessage(s, OK)
print('Enviando numero de paqetes recibidos: ', str(numPaquetesRecibidos))
sendOneMessage(s, str(numPaquetesRecibidos).encode())
print('Enviando bytes recibidos: ', str(bytesRecibidos))
sendOneMessage(s, str(bytesRecibidos).encode())
print('La integridad del archivo pudo ser verificada correctamente.')
print('Comando enviado: ', repr(OK))


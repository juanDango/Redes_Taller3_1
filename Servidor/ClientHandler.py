import socket
from threading import Thread
from socketserver import ThreadingMixIn
import struct
import datetime
import os
import hashlib
import sys

BUFFER_SIZE = 1024
BEG_RECV = b'BEG_RECV'
OK = b'OK'
ERR = b'ERR'
END_TRANSMISSION = b'END_TRANSMISSION'

class ClientHandler(Thread):
    def __init__(self, ip, port, sock, archivoElegido, log, scanner):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        self.archivoElegido = archivoElegido
        self.log = log
        self.scanner = scanner
        print('Iniciando un nuevo thread para ' + str(ip) +':' + str(port))

    def sendOneMessage(self, data):
        length = len(data)
        self.sock.sendall(struct.pack('!I', length))
        self.sock.sendall(data)

    def receiveAll(self, count):
        buf = b''
        while count:
            newbuf = self.sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def receiveOneMessage(self):
        lengthBuf = self.receiveAll(4)
        length, = struct.unpack('!I', lengthBuf)
        return self.receiveAll(length)
    
    def run(self):
        notifBeginCliente = self.receiveOneMessage()
        if (repr(notifBeginCliente) != repr(BEG_RECV)):
            print('El mensaje recibido es incorrecto. Finalizando conexion con: ', (self.ip, self.port))
            self.sendOneMessage(ERR)
            return
        print('Comando recibido: ', repr(notifBeginCliente))  

        print('Enviando comando: ', OK)
        self.sendOneMessage(OK)
        print('El servidor esta listo para enviar archivos.')
        print('Enviando comando con el nombre del archivo: ', self.archivoElegido)
        self.sendOneMessage(self.archivoElegido.encode())
        f = open(self.archivoElegido, 'rb')
        fechaInicioTransmision = 0
        digest = hashlib.md5()
        numPaquetesEnviados = 0
        bytesEnviados = 0
        while True:
            fechaInicioTransmision = datetime.datetime.now()
            print('Fecha inicio transmision archivo: ', fechaInicioTransmision)
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sendOneMessage(l)
                print('Se ha enviado: ', repr(l))
                digest.update(l)
                bytesEnviados += sys.getsizeof(l)
                l = f.read(BUFFER_SIZE)
                numPaquetesEnviados +=1
            if not l:
                f.close()
                print('Se ha completado la transferencia del archivo')       
                break
        print('Enviando comando: ', repr(END_TRANSMISSION))
        self.sendOneMessage(END_TRANSMISSION)
        fechaFinTransmision = self.receiveOneMessage()
        duracionTransmision = datetime.datetime.strptime(fechaFinTransmision.decode(), '%Y-%m-%d %H:%M:%S.%f') - fechaInicioTransmision
        print("La duracion total de la transmision fue de: %f s" %(duracionTransmision.total_seconds())) 
        #Mandamos el digest
        digestE = digest.hexdigest().encode()
        print(digestE)
        self.sendOneMessage(digestE)
        entregaExitosa = self.receiveOneMessage()
        numPaquetesRecibidos = repr(self.receiveOneMessage())[2:-1]
        bytesRecibidos = repr(self.receiveOneMessage())[2:-1]
        print('Comando recibido: ', repr(entregaExitosa))
        print('El cliente ' + self.ip + ':' + str(self.port) + ' recibio ' + numPaquetesRecibidos + ' paquetes')
        print('Numero de bytes enviados: ', bytesEnviados)
        print('El cliente ' + self.ip + ':' + str(self.port) + ' recibio ' + bytesRecibidos + ' bytes')
        stats = self.scanner.endConnection(self.ip, self.port)
        print(stats)
        #Format: ip:puerto;entregaExitosa;duracion_transmision;numPaquetesEnviados;numPaquetesRecibidos;totalBytesEnviados;totalBytesRecibidos;
        self.log.write(self.ip + ':' + str(self.port) + ';' + repr(entregaExitosa)[2:-1] + ';' + str(duracionTransmision.total_seconds()) + ';' +  
        str(numPaquetesEnviados)+ ';' + numPaquetesRecibidos +  ';' + str(bytesEnviados) + ';' + bytesRecibidos +  ';\n')
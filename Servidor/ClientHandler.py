import socket
from threading import Thread
from socketserver import ThreadingMixIn
import struct

BUFFER_SIZE = 1024
BEG_RECV = b'BEG_RECV'
OK = b'OK'
FILE_OPTS = b'FILE_OPTS'
FILENAMES_SENT = b'FILENAMES_SENT'
ERR = b'ERR'

files = ['./files/prueba1.txt', './files/prueba2.txt']

class ClientHandler(Thread):
    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
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

        print('Enviando comando: ', FILE_OPTS)
        self.sendOneMessage(FILE_OPTS)
        print('Enviando nombres de archivos al cliente')

        for opt in files:
            self.sendOneMessage(opt.encode())

        self.sendOneMessage(FILENAMES_SENT)
        print('Envio de nombres de archivos finalizado')

        try:
            archivoElegido = int(repr(self.receiveOneMessage())[2:-1])
            print('Se ha elegido el archivo: ' + repr(files[archivoElegido]))
            self.sendOneMessage(OK)
        except:
            print('Archivo no disponible. Cerrando la conexion con: ', (self.ip, self.port))
            self.sendOneMessage(ERR)
            return





"""
        filename = 'data/prueba.txt'
        f = open(filename, 'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                print('Se ha enviado: ', repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break
"""
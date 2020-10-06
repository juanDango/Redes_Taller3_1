import socket
from threading import Thread
from socketserver import ThreadingMixIn

BUFFER_SIZE = 1024
BEG_RECV = b'BEG_RECV'
OK = b'OK'
FILE_OPTS = b'FILE_OPTS'
FILENAMES_SENT = b'FILENAMES_SENT'

files = [b'./files/prueba1.txt', b'./files/prueba2.txt']

class ClientHandler(Thread):
    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print('Iniciando un nuevo thread para ' + str(ip) +':' + str(port))
    
    def run(self):
        notifBeginCliente = self.sock.recv(BUFFER_SIZE)
        if (repr(notifBeginCliente) != repr(BEG_RECV)):
            print('El mensaje recibido es incorrecto. Finalizando conexion con: ', (self.ip, self.port))
            return
        print('Comando recibido: ', repr(notifBeginCliente))  

        print('Enviando comando: ', OK)
        self.sock.send(OK)
        print('El servidor esta listo para enviar archivos.')

        print('Enviando comando: ', FILE_OPTS)
        self.sock.send(FILE_OPTS)
        print('Enviando nombres de archivos al cliente')
        for opt in files:
            self.sock.send(opt)
        self.sock.send(FILENAMES_SENT)
        print('Envio de nombres de archivos finalizado')

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
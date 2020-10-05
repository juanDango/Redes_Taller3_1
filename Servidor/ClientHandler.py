import socket
from threading import Thread
from socketserver import ThreadingMixIn

BUFFER_SIZE = 1024

class ClientHandler(Thread):
    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print('Iniciando un nuevo thread para ' + str(ip) +':' + str(port))
    
    def run(self):
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
        
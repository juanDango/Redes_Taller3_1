import socket
from threading import Thread
from socketserver import ThreadingMixIn
from ClientHandler import ClientHandler

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    #Socket que permite al servidor escuchar las peticiones de los clientes.
    tcpsock.listen()
    print('El servidor esta esperando conexiones...')
    (conn, (ip,port)) = tcpsock.accept()
    print('Se recibio una conexion de: ', (ip, port))
    newthread = ClientHandler(ip, port, conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()




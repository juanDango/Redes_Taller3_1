import socket
import os
from threading import Thread
from socketserver import ThreadingMixIn
from ClientHandler import ClientHandler
import datetime

EC2_PUBLIC_IP = '54.91.103.85'
TCP_IP = socket.gethostbyaddr(EC2_PUBLIC_IP)[0]
TCP_PORT = 60001


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

path = './files/'
files = os.listdir(path)
files.remove('.DS_Store')

numClientes = int(input('Indique el numero maximo de clientes a conectar: '))
print('Los archivos disponibles en el servidor son: ')

for i in range(len(files)):
    print(str(i+1) + '. ' + files[i]) 

j = 0
try:
    j = int(input('Escoja el numero de archivo a enviar: \n')) - 1
except:
    print('Opcion incorrecta.')
    tcpsock.close()
    exit()

archivoElegido = files[j]
fechaPrueba = str(datetime.datetime.now())
log = open(fechaPrueba + '.log', 'w')
log.write('Fecha y Hora: ' + fechaPrueba + '\n')
log.write('Nombre Archivo: ' + archivoElegido + '\n')
log.write('Tamaño Archivo: ' + str(os.path.getsize(path + archivoElegido)) + '\n' )


for i in range(numClientes):
    #Socket que permite al servidor escuchar las peticiones de los clientes.
    tcpsock.listen()
    print('El servidor esta esperando conexiones...')
    (conn, (ip,port)) = tcpsock.accept()
    print('Se recibio una conexion de: ', (ip, port))
    newthread = ClientHandler(ip, port, conn, path + archivoElegido, log)
    threads.append(newthread)   

for t in threads:
    t.start()







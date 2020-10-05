#!/usr/bin/env python3

import socket

PORT = 65432

#Creamos un socket que funciona con IPv4 (socket.AF_INET) y se comunica por medio del protocolo TCP (socket.SOCK_STREAM)
#Usamos la instruccion with para evitar la instruccion socket.close() al finalizar la ejecucion.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    HOST = socket.gethostname()
    #Bind se encarga de unir un host con un puerto determinado. 
    s.bind((HOST, PORT))
    #Socket que permite al servidor escuchar las peticiones de los clientes.
    s.listen()
    print('El servidor esta esperando conexiones...')
    while True:
        #Accept bloquea y espera a una nueva conexion. Como usamos IPv4, retorna una tupla con la conexion del cliente y su direccion.
        #Se crea un nuevo socket que se usara para comunicarse con cada cliente. Es diferente del socket de listen().
        conn, address = s.accept()
        with conn:
            print('Se recibio una conexion de: ', address)
            data = conn.recv(1024)
            print('El servidor ha recibido: ', repr(data))

            filename = 'data/prueba.txt'
            with open(filename, 'rb') as f:
                l = f.read(1024)
                while (l):
                    conn.send(l)
                    print('Sent ', repr(l))
                    l = f.read(1024)
            print('Se ha finalizado el envio de datos')
            conn.send(b'Gracias por conectarte a nuestro servidor.\n Ten un gran dia.\n Que no te de coronavirus.\n Con amor,\n Servidor Don Jose Stalin')



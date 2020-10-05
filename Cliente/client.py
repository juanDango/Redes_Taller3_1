#!/usr/bin/env python3

import socket

PORT = 65432 # El puerto usado por el servidor

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    HOST = socket.gethostname() # La IP del servidor
    s.connect((HOST, PORT))
    #Envia un mensaje de conexion al servidor
    s.send((b'Hola, querido servidor'))

    with open('archivo_recibido', 'wb') as f:
        print('Se ha abierto el archivo')
        while True:
            print('Recibiendo los datos')
            #Recibe la respuesta del servidor
            datos = s.recv(1024)
            #Imprime la respuesta del servidor
            print('Datos recibidos: ', repr(datos))
            if not datos:
                break
            f.write(datos)
    
    print('Se ha recibido el archivo satisfactoriamente')
print('Se ha cerrado la conexion')







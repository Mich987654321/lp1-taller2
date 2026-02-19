#!/usr/bin/env python3
"""
Problema 1: Sockets básicos - Servidor
Objetivo: Crear un servidor TCP que acepte una conexión y intercambie mensajes básicos
"""

import socket

#Definir la dirección y puerto del servidor
HOST = 'Localhost'
PORT = 9001

#Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Enlazar el socket a la dirección y puerto especificados
servidor.bind((HOST, PORT))

# Poner el socket en modo escucha
servidor.listen()
# El parámetro define el número máximo de conexiones en cola
print("Servidor a la espera de conexiones ...")

# Aceptar una conexión entrante
conn, addr = servidor.accept()()  
print(f"Conexión realizada por {addr}")
# accept() bloquea hasta que llega una conexión
# conn: nuevo socket para comunicarse con el cliente
# addr: dirección y puerto del cliente

#Recibir datos del cliente (hasta 1024 bytes)
datos = conn.recv(1024) 
print(f"El cliente envió: {datos.decode()}") 

# Enviar respuesta al cliente (convertida a bytes)
# sendall() asegura que todos los datos sean enviados
mensaje_inicial = b"Hola, cliente. Bienvenido al servidor."
conn.sendall(mensaje_inicial)

# Cerrar la conexión con el cliente
conn.close()
servidor.close()
print("Servidor cerrado")
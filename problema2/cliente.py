#!/usr/bin/env python3
"""
Problema 2: Comunicación bidireccional - Cliente
Objetivo: Crear un cliente TCP que envíe un mensaje al servidor y reciba la misma respuesta
"""

import socket

#Definir la dirección y puerto del servidor
HOST = 'localhost'
PORT = 8000

# Solicitar mensaje al usuario por consola
message = input("Mensaje: ")

# Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conectar el socket al servidor en la dirección y puerto especificados
HOST = 'Localhost'
PORT = 8000
cliente.connect((HOST, PORT))
print("Conexión con éxito")

# Mostrar mensaje que se va a enviar
print(f"Mensaje '{message}' enviado.")

#Codificar el mensaje a bytes y enviarlo al servidor
# sendall() asegura que todos los datos sean enviados
cliente.sendall(b"Mundo")

#Recibir datos del servidor (hasta 1024 bytes)
datos = cliente.recv(1024)
print(f"Respuesta: {datos}")

# Decodificar e imprimir los datos recibidos
print("Mensaje recibido: ", datos.decode())

#Cerrar la conexión con el servidor
cliente.close()


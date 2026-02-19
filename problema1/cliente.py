#!/usr/bin/env python3
"""
Problema 1: Sockets básicos - Cliente
Objetivo: Crear un cliente TCP que se conecte a un servidor e intercambie mensajes básicos
"""
import socket

#Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    

#Conectar el socket al servidor en la dirección y puerto especificados
HOST = 'Localhost'
PORT = 9001
cliente.connect((HOST, PORT))
print("Conexión con éxito")

#Enviar datos al servidor (convertidos a bytes)
# sendall() asegura que todos los datos sean enviados
cliente.sendall(b"Mundo")

#Recibir datos del servidor (hasta 1024 bytes)
datos = cliente.recv(1024)
print(f"Respuesta: {datos}")

#Decodificar e imprimir los datos recibidos
print("El servidor indica", datos.decode())

#Cerrar la conexión con el servidor
cliente.close()

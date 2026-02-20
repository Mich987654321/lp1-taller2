#!/usr/bin/env python3
"""
Problema 3: Chat simple con múltiples clientes - Servidor
Objetivo: Crear un servidor de chat que maneje múltiples clientes simultáneamente usando threads
"""

import socket
import threading

#Definir la dirección y puerto del servidor

HOST = 'Localhost' 
PORT = 9000

# Lista para mantener todos los sockets de clientes conectados
clients = []

def handle_client(client_socket, client_name):
    """
    Maneja la comunicación con un cliente específico en un hilo separado.
    
    Args:
        client_socket: Socket del cliente
        client_name: Nombre del cliente
    """
    while True:
        try:
            #Recibir datos del cliente (hasta 1024 bytes)
            data = client_socket.recv(1024)
            
            # Si no se reciben datos, el cliente se desconectó
            if not data:
                break

            # Formatear el mensaje con el nombre del cliente
            message = f"{client_name}: {data.decode()}"
            
            # Imprimir el mensaje en el servidor
            print(message)
            
            # Retransmitir el mensaje a todos los clientes excepto al remitente
            broadcast(message, client_socket)              
        except ConnectionResetError:
       
            # Manejar desconexión inesperada del cliente
            clients.remove(client_socket)
            client_socket.close()
            break   

def broadcast(message, sender_socket):
    """
    Envía un mensaje a todos los clientes conectados excepto al remitente.
    
    Args:
        message: Mensaje a enviar (string)
        sender_socket: Socket del cliente que envió el mensaje original
    """
    for client in clients:
     if client != sender_socket:
        client.send(message.encode())
    #Enviar el mensaje codificado a bytes a cada cliente
      

# Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Enlazar el socket a la dirección y puerto especificados
HOST = 'Localhost'
PORT = 9000

servidor.bind((HOST, PORT))

# Poner el socket en modo escucha
servidor.listen()

# El parámetro define el número máximo de conexiones en cola
print("Servidor a la espera de conexiones ...")

# Bucle principal para aceptar conexiones entrantes
while True:
    # Aceptar una conexión entrante
    # client: nuevo socket para comunicarse con el cliente
    # addr: dirección y puerto del cliente

    conn, addr = servidor.accept()
    print(f"Conexión realizada por {addr}")

    # Recibir el nombre del cliente (hasta 1024 bytes) y decodificarlo
    name = conn.recv(1024).decode()

    # Agregar el socket del cliente a la lista de clientes conectados
    clients.append(conn)

    # Enviar mensaje de confirmación de conexión al cliente
    conn.send("ya estás conectado!".encode())
    
    # Notificar a todos los clientes que un nuevo usuario se unió al chat
    broadcast(f"{name} se ha unido al Chat.", conn)
    
    #Crear e iniciar un hilo para manejar la comunicación con este cliente
    # target: función que se ejecutará en el hilo
    # args: argumentos que se pasarán a la función
    hilo_client = threading.Thread(target=handle_client, args=(conn, name))
    hilo_client.start()


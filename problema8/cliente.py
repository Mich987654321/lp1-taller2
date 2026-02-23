import socket
import threading

# Cliente sencillo para jugar desde la terminal
nombre = input("¿Cual es tu nombre de jugador? ")
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 6000))

def escuchar_servidor():
    while True:
        try:
            dato = cliente.recv(2048).decode('utf-8')
            if dato == "DIME_NOMBRE":
                cliente.send(nombre.encode('utf-8'))
            else:
                print(dato) # Aquí imprimimos el tablero o los avisos del server
        except:
            print("Se cayó la conexión con el servidor.")
            break

# Hilo para recibir mensajes sin bloquear el teclado
threading.Thread(target=escuchar_servidor, daemon=True).start()

print("Para jugar, escribe un numero del 0 al 8 y dale Enter.")
while True:
    try:
        movimiento = input() # Leemos la jugada del usuario
        cliente.send(movimiento.encode('utf-8'))
    except:
        break
import socket
import threading

# 1. Configuración inicial
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 5001))

# 2. ESPERAR el mensaje del servidor antes de hacer cualquier otra cosa
signal = cliente.recv(1024).decode('utf-8')
if signal == "DIME_TU_NOMBRE":
    mi_nombre = input("Escribe tu nickname: ")
    cliente.send(mi_nombre.encode('utf-8'))

# 3. Ahora sí, definimos las funciones normales
def escuchar():
    while True:
        try:
            msg = cliente.recv(1024).decode('utf-8')
            print(f"\n{msg}")
        except:
            break

def escribir():
    while True:
        msg = input("> ")
        cliente.send(msg.encode('utf-8'))

# 4. Lanzamos los hilos solo cuando ya estamos identificados
threading.Thread(target=escuchar, daemon=True).start()
escribir()
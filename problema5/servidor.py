import socket
import os
import hashlib
import threading

HOST = 'localhost'
PORT = 8005
BUFFER_SIZE = 4096
BASE_DIR = "archivos_servidor"

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

def calcular_checksum(ruta_archivo):
    hash_sha256 = hashlib.sha256()
    with open(ruta_archivo, "rb") as f:
        for bloque in iter(lambda: f.read(BUFFER_SIZE), b""):
            hash_sha256.update(bloque)
    return hash_sha256.hexdigest()

def manejar_cliente(conn, addr):
    print(f"[+] Conexión desde: {addr}")
    try:
        # LEER EL COMANDO (UPLOAD nombre tamano)
        datos = conn.recv(1024).decode().strip()
        if not datos: return

        partes = datos.split()
        if partes[0].upper() == "UPLOAD":
            nombre = os.path.basename(partes[1])
            tamano = int(partes[2])
            ruta_final = os.path.join(BASE_DIR, nombre)

            # Recibir los bytes de archivo
            with open(ruta_final, "wb") as f:
                recibido = 0
                while recibido < tamano:
                    # Leemos solo lo que falta para no pasarnos al siguiente comando
                    chunk = conn.recv(min(BUFFER_SIZE, tamano - recibido))
                    if not chunk: break
                    f.write(chunk)
                    recibido += len(chunk)

            # Calculo de huella
            huella = calcular_checksum(ruta_final)
            conn.send(f"OK:{huella}".encode())
            print(f"[!] Archivo {nombre} guardado y verificado.")

    except Exception as e:
        print(f"[-] Error procesando cliente: {e}")
    finally:
        conn.close()

# Configuración del Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)
print(f"[*] SERVIDOR ACTIVO EN PUERTO {PORT}...")

while True:
    conex, addr = server.accept()
    threading.Thread(target=manejar_cliente, args=(conex, addr)).start()
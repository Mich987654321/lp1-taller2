import socket 
import os
import hashlib
import time

HOST = 'localhost' 
PORT = 8005
BUFFER_SIZE = 4096

def calcular_checksum(ruta_archivo):
    hash_sha256 = hashlib.sha256()
    with open(ruta_archivo, "rb") as f:
        for bloque in iter(lambda: f.read(BUFFER_SIZE), b""):
            hash_sha256.update(bloque)
    return hash_sha256.hexdigest()

def enviar_archivo(nombre_archivo):
    #  Verificar si existe, luego el tamaño
    if not os.path.exists(nombre_archivo):
        print(f"[-] Error: El archivo '{nombre_archivo}' no existe")
        return
    
    tamano = os.path.getsize(nombre_archivo)
    checksum_local = calcular_checksum(nombre_archivo)

    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))

        #  Enviar comando
        print(f"[*] Solicitando UPLOAD de {nombre_archivo} ({tamano} bytes)...")
        comando = f"UPLOAD {nombre_archivo} {tamano}\n"
        cliente.send(comando.encode())

        #  Pausa para sincronización
        time.sleep(0.1)

        #  Enviar contenido binario
        with open(nombre_archivo, "rb") as f:
            while (bloque := f.read(BUFFER_SIZE)):
                cliente.sendall(bloque)

        #  Recibir respuesta del Servidor
        respuesta = cliente.recv(1024).decode()
        
        if respuesta.startswith("OK:"):
            checksum_servidor = respuesta.split(":")[1]
            print(f"[+] Servidor recibió el archivo.")
            print(f"[*] Checksum Local:    {checksum_local}")
            print(f"[*] Checksum Servidor: {checksum_servidor}")
            
            if checksum_local == checksum_servidor:
                print("¡ÉXITO! Integridad verificada.")
            else:
                print("ALERTA: El archivo se corrompió.")
        
        cliente.close()

    except Exception as e:
        print(f"[-] Error de conexión: {e}")

# Ejecución de prueba
if __name__ == "__main__":
    with open("prueba.txt", "w") as f:
        f.write("Este es el contenido del archivo para el Problema 5.")
    enviar_archivo("prueba.txt")
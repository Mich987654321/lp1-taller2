import socket

# Configuracion
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 8080
URL_DESTINO = 'www.google.com' # Vamos a pedir la landing de Google

def cliente_peticion():
    try:
        #  Nos conectamos al PROXY, no a Google directamente
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((PROXY_HOST, PROXY_PORT))
        
        #  Armamos una peticion HTTP manual
        # El proxy necesita la URL completa para saber a donde ir
        peticion = (
            f"GET http://{URL_DESTINO}/ HTTP/1.1\r\n"
            f"Host: {URL_DESTINO}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        
        print(f"[*] Enviando peticion al proxy para ir a {URL_DESTINO}...")
        sock.sendall(peticion.encode())
        
        #  Recibimos la respuesta que el proxy nos trajo del servidor real
        respuesta = b""
        while True:
            datos = sock.recv(4096)
            if not datos: break
            respuesta += datos
        
        # Mostramos los primeros 200 caracteres de lo que nos devolvio el servidor real
        print("\n[+] Respuesta recibida del Proxy:")
        print("-" * 30)
        print(respuesta.decode('utf-8', errors='ignore')[:500] + "...")
        print("-" * 30)
        
        sock.close()
    except Exception as e:
        print(f"[!] Error en el cliente: {e}")

if __name__ == "__main__":
    cliente_peticion()
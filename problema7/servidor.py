import socket
import threading

class ProxyServer:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"[*] Proxy escuchando en {self.host}:{self.port}")

    def tunel(self, origen, destino):
        # Pasa los bytes de un socket a otro hasta que uno se cierre
        try:
            while True:
                data = origen.recv(4096)
                if not data: break
                destino.sendall(data)
        except:
            pass # Si se corta la conexion, ni modo
        finally:
            origen.close()
            destino.close()

    def gestionar_cliente(self, client_sock):
        try:
            # Leer la peticion inicial del cliente
            request = client_sock.recv(4096)
            if not request: return
            
            #  Extraer el host 
            primera_linea = request.decode('utf-8', errors='ignore').split('\n')[0]
            print(f"[>] Peticion: {primera_linea}")
            
            # Sacamos el host y el puerto (super manual para que se entienda)
            url = primera_linea.split(' ')[1]
            if "://" in url: url = url.split("://")[1]
            host = url.split('/')[0]
            puerto = 80 # Por defecto HTTP
            
            if ":" in host:
                puerto = int(host.split(":")[1])
                host = host.split(":")[0]

            # Conectar con el servidor destino real
            print(f"[*] Conectando al destino: {host}:{puerto}")
            remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_sock.connect((host, puerto))

            #  Si es HTTPS (CONNECT), avisamos al cliente. Si es HTTP, reenviamos la peticion.
            if "CONNECT" in primera_linea:
                client_sock.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            else:
                remote_sock.sendall(request)

            # Creamos el puente bidireccional
            # Hilo A: Cliente -> Proxy -> Servidor Real
            # Hilo B: Servidor Real -> Proxy -> Cliente
            threading.Thread(target=self.tunel, args=(client_sock, remote_sock)).start()
            threading.Thread(target=self.tunel, args=(remote_sock, client_sock)).start()

        except Exception as e:
            print(f"[!] Error gestionando cliente: {e}")
            client_sock.close()

    def iniciar(self):
        while True:
            client, addr = self.server.accept()
            threading.Thread(target=self.gestionar_cliente, args=(client,)).start()

if __name__ == "__main__":
    ProxyServer().iniciar()
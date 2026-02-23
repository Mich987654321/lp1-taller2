import http.server
import socketserver
import sys

# Pillamos el puerto de la consola (ej: python backend.py 8081)
if len(sys.argv) < 2:
    print("Error: Pon un puerto, no seas gollipollas")
    sys.exit(1)

PORT = int(sys.argv[1])

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            # El "Health Check" para decirle al balanceador que estamos vivos
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK - Vivo y coleando")
        elif self.path == '/trabajo':
            # Aquí es donde el cliente pide la data real
            self.send_response(200)
            self.end_headers()
            respuesta = f"Respuesta desde el servidor en puerto {PORT}"
            self.wfile.write(respuesta.encode())
        else:
            self.send_error(404, "Aqui no hay nada, compa")

print(f"🟢 Backend encendido en el puerto {PORT}...")
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    httpd.serve_forever()
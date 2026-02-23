import socket
import threading

# Mi servidor de chat con salas
# Para que funcione: necesito guardar quien es quien y en que sala esta
class ServidorChat:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5001
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        
        # Aqui guardo todo el relajo
        self.clientes = {}      # {socket: nombre}
        self.salas = {"general": []} # {nombre_sala: [lista_de_sockets]}
        self.ubicacion = {}     # {socket: sala_actual}
        
        print("Servidor prendido... esperando gente")

    def enviar_a_sala(self, msg, nombre_sala, origen=None):
        # Funcion para no repetir codigo al mandar mensajes a un grupo
        if nombre_sala in self.salas:
            for socket_cliente in self.salas[nombre_sala]:
                if socket_cliente != origen: # No me lo mandes a mi mismo
                    try:
                        socket_cliente.send(msg.encode('utf-8'))
                    except:
                        self.desconectar(socket_cliente)

    def comandos(self, cliente, texto):
        # Aqui manejo los /join y esas cosas
        partes = texto.split(' ')
        cmd = partes[0].lower()

        if cmd == "/join" or cmd == "/create":
            nueva_sala = partes[1]
            
            # Primero lo saco de donde estaba
            sala_vieja = self.ubicacion.get(cliente)
            if sala_vieja:
                self.salas[sala_vieja].remove(cliente)
                self.enviar_a_sala(f"SISTEMA: {self.clientes[cliente]} se fue a otra sala.", sala_vieja)

            # Si la sala no existe, la invento ahorita
            if nueva_sala not in self.salas:
                self.salas[nueva_sala] = []
            
            self.salas[nueva_sala].append(cliente)
            self.ubicacion[cliente] = nueva_sala
            cliente.send(f"SISTEMA: Entraste a '{nueva_sala}'".encode('utf-8'))
            self.enviar_a_sala(f"SISTEMA: {self.clientes[cliente]} entro a la sala.", nueva_sala, cliente)

        elif cmd == "/private":
            # Formato: /private usuario mensaje
            destino = partes[1]
            mensaje_priv = " ".join(partes[2:])
            
            encontrado = False
            for sock, nick in self.clientes.items():
                if nick == destino:
                    sock.send(f"[PRIVADO de {self.clientes[cliente]}]: {mensaje_priv}".encode('utf-8'))
                    encontrado = True
                    break
            if not encontrado:
                cliente.send("SISTEMA: No encontre a ese usuario.".encode('utf-8'))

    def atender_cliente(self, cliente):
        while True:
            try:
                data = cliente.recv(1024).decode('utf-8')
                if not data: break
                
                if data.startswith('/'):
                    self.comandos(cliente, data)
                else:
                    # Mensaje normal, solo a mi sala
                    mi_sala = self.ubicacion[cliente]
                    formato = f"({mi_sala}) {self.clientes[cliente]}: {data}"
                    self.enviar_a_sala(formato, mi_sala, cliente)
            except:
                self.desconectar(cliente)
                break

    def desconectar(self, cliente):
        # Limpieza cuando alguien cierra el programa
        if cliente in self.clientes:
            print(f"Chao a {self.clientes[cliente]}")
            sala = self.ubicacion.get(cliente)
            if sala:
                self.salas[sala].remove(cliente)
            del self.clientes[cliente]
            del self.ubicacion[cliente]
            cliente.close()

    def iniciar(self):
        while True:
            conn, addr = self.server.accept()
            # Lo primero que le pido es el nombre
            conn.send("DIME_TU_NOMBRE".encode('utf-8'))
            nombre = conn.recv(1024).decode('utf-8')
            
            self.clientes[conn] = nombre
            self.ubicacion[conn] = "general"
            self.salas["general"].append(conn)
            
            print(f"{nombre} se conecto desde {addr}")
            
            # Un hilo por cada persona para que no se trabe
            thread = threading.Thread(target=self.atender_cliente, args=(conn,))
            thread.start()

if __name__ == "__main__":
    server = ServidorChat()
    server.iniciar()
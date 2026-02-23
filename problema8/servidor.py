import socket
import threading

# Problema 8: El servidor que controla el tablero
class ServidorJuego:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 6000
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen()

        # El estado global: una lista simple de 9 espacios
        self.tablero = [" "] * 9 
        self.jugadores = []      # Los dos primeros que lleguen a jugar
        self.espectadores = []   # El resto solo mira
        self.turno = 0           # Empezamos con el Jugador X (posicion 0)
        
        print("Listo, el servidor de Triqui ya está corriendo...")

    def dibujar_tablero(self):
        # Un dibujo básico para que se vea algo en la terminal
        t = self.tablero
        return f"\n {t[0]} | {t[1]} | {t[2]} \n-----------\n {t[3]} | {t[4]} | {t[5]} \n-----------\n {t[6]} | {t[7]} | {t[8]} \n"

    def verificar_ganador(self):
        t = self.tablero
        # Combinaciones ganadoras (filas, columnas, diagonales)
        lineas = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        
        for a, b, c in lineas:
            if t[a] == t[b] == t[c] and t[a] != " ":
                return t[a]
        if " " not in t:
            return "Empate"
        return None

    def avisar_a_todos(self, mensaje):
        # Hay que mandarle el estado a todo el mundo (jugadores y los que miran)
        for s in self.jugadores + self.espectadores:
            try:
                s.send(mensaje.encode('utf-8'))
            except:
                pass # Si alguien se desconecto, lo ignoramos por ahora

    def atender_jugador(self, conn):
        while True:
            try:
                msg = conn.recv(1024).decode('utf-8')
                if not msg: break
                
                # Chequeo rápido: ¿Quién está mandando el mensaje?
                yo_soy_x = (conn == self.jugadores[0] if len(self.jugadores) > 0 else False)
                yo_soy_o = (conn == self.jugadores[1] if len(self.jugadores) > 1 else False)
                
                # ¿Es el turno del que mandó el mensaje?
                le_toca = (self.turno == 0 and yo_soy_x) or (self.turno == 1 and yo_soy_o)
                
                if le_toca:
                    pos = int(msg) # Ojo: asumimos que el cliente manda un numero del 0-8
                    if self.tablero[pos] == " ":
                        self.tablero[pos] = "X" if self.turno == 0 else "O"
                        self.turno = 1 - self.turno # Cambiamos el turno (0 <-> 1)
                        
                        resultado = self.verificar_ganador()
                        if resultado:
                            self.avisar_a_todos(self.dibujar_tablero() + f"\nResultado: {resultado}")
                            self.tablero = [" "] * 9 # Limpiamos para la otra partida
                        else:
                            self.avisar_a_todos(self.dibujar_tablero() + f"\nSigue: {'X' if self.turno == 0 else 'O'}")
                    else:
                        conn.send("Esa casilla ya está marcada, elige otra.".encode('utf-8'))
                else:
                    conn.send("Tranquilo, no es tu turno todavia.".encode('utf-8'))
            except:
                # Si alguien cierra la terminal o falla el internet, limpiamos todo
                print("Alguien se desconectó. Limpiando tablero para el siguiente juego...")
                self.tablero = [" "] * 9
                self.jugadores = [] 
                self.espectadores = []
                self.turno = 0 #  Que vuelva a empezar el Jugador X
                break

    def iniciar(self):
        while True:
            conn, addr = self.server.accept()
            conn.send("DIME_NOMBRE".encode('utf-8'))
            nombre = conn.recv(1024).decode('utf-8')
            
            # Lógica de entrada: los 2 primeros juegan, el resto mira
            if len(self.jugadores) < 2:
                self.jugadores.append(conn)
                ficha = "X" if len(self.jugadores) == 1 else "O"
                conn.send(f"Bienvenido {nombre}. Juegas con la: {ficha}".encode('utf-8'))
            else:
                self.espectadores.append(conn)
                conn.send(f"Hola {nombre}, ya hay dos jugando. Te toca mirar.".encode('utf-8'))
            
            # Mandamos el tablero inicial
            conn.send(self.dibujar_tablero().encode('utf-8'))
            threading.Thread(target=self.atender_jugador, args=(conn,)).start()

if __name__ == "__main__":
    ServidorJuego().iniciar()
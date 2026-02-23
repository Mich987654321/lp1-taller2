import threading
import time
import requests # Vas a necesitar: pip install requests
from flask import Flask # Vas a necesitar: pip install flask

app = Flask(__name__)

# Lista de servidores a coordinar
servidores = [
    {"url": "http://localhost:8081", "vivo": True},
    {"url": "http://localhost:8082", "vivo": True}
]
indice_actual = 0
lock = threading.Lock() # Para que el Round Robin sea seguro entre hilos

def health_check():
    """ Revisa cada 10 segundos si los nodos siguen respirando """
    global servidores
    while True:
        for s in servidores:
            try:
                # Intentamos conectar al endpoint de salud
                response = requests.get(s["url"] + "/health", timeout=2)
                if response.status_code == 200:
                    if not s["vivo"]:
                        print(f"✅ Nodo {s['url']} ha vuelto a la vida.")
                    s["vivo"] = True
                else:
                    s["vivo"] = False
            except:
                if s["vivo"]:
                    print(f"❌ Nodo {s['url']} se fue al carajo.")
                s["vivo"] = False
        time.sleep(10)

@app.route('/')
def balancear():
    global indice_actual
    
    # Buscamos el siguiente servidor vivo (Round Robin)
    with lock:
        for _ in range(len(servidores)):
            s = servidores[indice_actual]
            indice_actual = (indice_actual + 1) % len(servidores)
            
            if s["vivo"]:
                try:
                    # Le pedimos la info al backend y se la pasamos al cliente
                    resp = requests.get(s["url"] + "/trabajo")
                    return resp.text
                except:
                    continue
        
        return "Error 503: No hay servidores vivos. ¡Corran por sus vidas!", 503

if __name__ == "__main__":
    # Lanzamos el health check en un hilo aparte (Daemon para que muera al cerrar el script)
    t = threading.Thread(target=health_check, daemon=True)
    t.start()
    
    print("🚀 Balanceador de carga corriendo en http://localhost:8080")
    app.run(port=8080)
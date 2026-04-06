import socket
import threading
import time

cliente = None
conectado = False

def recibir_mensajes():
    global conectado
    while True:
        if not conectado or cliente is None:
            time.sleep(0.5)  # Espera hasta que haya conexión
            continue
        try:
            mensaje = cliente.recv(1024).decode("utf-8")
            if mensaje:
                print(f"\n[Mensaje recibido]: {mensaje}")
                print("Escriba su mensaje: ", end="", flush=True)
            else:
                # Servidor cerró la conexión limpiamente
                print("\n[Servidor desconectado]")
                conectado = False
        except:
            # Error de señal, red caída, etc.
            conectado = False

 # Hilo dedicado a mantener la conexión activa
def hilo_conexion():
   
    global cliente, conectado
    server_ip = "127.0.0.1"
    server_port = 8000

    while True:  # Bucle de reconexión
        if not conectado:
            try:
                print("[Conectando al servidor...]")
                cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                cliente.connect((server_ip, server_port))
                conectado = True
                print("[Conectado!]")
            except Exception as e:
                print(f"[Error al conectar: {e}. \nReintentando en 3s...]")
                time.sleep(3)  # Espera antes de reintentar

        time.sleep(1)  # Revisa el estado cada 1 segundo

def run_client():

    global conectado
    
    nombre = input("Ingresa tu nombre: ")

    # Hilo que mantiene la conexión
    thread_conexion = threading.Thread(target=hilo_conexion)
    thread_conexion.daemon = True
    thread_conexion.start()

    # Hilo que recibe mensajes
    thread_recibir = threading.Thread(target=recibir_mensajes)
    thread_recibir.daemon = True
    thread_recibir.start()

    # Bucle principal: enviar mensajes
    while True:
        msg = input("Escriba su mensaje: ")

        if not conectado:
            print("[Sin conexión, espere...]")
            continue

        if msg.lower() == "close":
            cliente.send("close".encode("utf-8"))
            break

        try:
            cliente.send(f"{nombre}: {msg}".encode("utf-8"))
        except:
            print("[Error al enviar, reconectando...]")
            conectado = False  # El hilo de conexión se encarga del resto

if __name__ == "__main__":
    run_client()
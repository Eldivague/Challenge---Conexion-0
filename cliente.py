import socket
import threading
import time        # se importa time para los intentos por error de conexion

# Función que corre en un hilo separado solo para recibir datos.
def recibir_mensajes(cliente_socket):
    while True:
        try:
            # Recibir mensaje del servidor
            mensaje = cliente_socket.recv(1024).decode("utf-8")
            if mensaje:
                print(f"\n[Mensaje recibido]: {mensaje}")
                print("Escriba su mensaje: ", end="", flush=True) # Para que no se pierda el prompt del input
            else:
                # Si el servidor cierra la conexión
                break
        except:
            print("Error recibiendo datos del servidor.")
            break

# Funcion para conectarse al servidor
def run_client():
    server_ip = "127.0.0.1"
    server_port = 8000
    nombre_del_cliente = input("ingresa tu nombre: ")
    intentos = 5
    
    # Se definen 5 intentos por si hay problemas de coneccion 
    for i in range(intentos):
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((server_ip, server_port))
            print("Conectado al servidor.")
            break
        except Exception as e:
            cliente.close()
            print(f"error : {e} ")
            print(f"No se pudo conectar. Intento {i+1}/{intentos}. Reintentando en 3s...")
            time.sleep(3)
    else:
        print("No se pudo conectar después de varios intentos. Saliendo.")
        return
    
    try:
        # Creamos un hilo para recibir mensajes mientras nosotros escribimos
        recibir_thread = threading.Thread(target=recibir_mensajes, args=(cliente,))
        recibir_thread.daemon = True # Esto hace que el hilo muera si cerramos el programa
        recibir_thread.start()

        # Bucle para mandar mensajes
        while True:
            msg = input("Escriba su mensaje: ")
            if msg.lower() == "close": # si se manda "close" se cierra la conexion
                cliente.send("close".encode("utf-8"))
                break
            
            cliente.send(f"{nombre_del_cliente}: {msg}".encode("utf-8"))
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cliente.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    run_client()
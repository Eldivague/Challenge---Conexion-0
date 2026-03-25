import socket
import threading

# Función que corre en un hilo separado solo para recibir datos.
def recibir_mensajes(cliente_socket):
    while True:
        try:
            # Recibir mensaje del servidor
            mensaje = cliente_socket.recv(1024).decode("utf-8")
            if mensaje:
                print(f"\n[Mensaje recibido]: {mensaje}")
                print("Enter mensaje: ", end="") # Para que no se pierda el prompt del input
            else:
                # Si el servidor cierra la conexión
                break
        except:
            print("Error recibiendo datos del servidor.")
            break

def run_client():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 8000
    nombre_del_cliente = input("ingresa tu nombre: ")
    try:
        cliente.connect((server_ip, server_port))
        print("Conectado al servidor.")

        # Creamos un hilo para recibir mensajes mientras nosotros escribimos
        receive_thread = threading.Thread(target=recibir_mensajes, args=(cliente,))
        receive_thread.daemon = True # Esto hace que el hilo muera si cerramos el programa
        receive_thread.start()

        while True:
            msg = input("Escriba su mensaje: ")
            if msg.lower() == "close":
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
import socket
import threading

def receive_messages(client_socket):
    """Función que corre en un hilo separado solo para recibir datos."""
    while True:
        try:
            # Recibir mensaje del servidor
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"\n[Mensaje recibido]: {message}")
                print("Enter message: ", end="") # Para que no se pierda el prompt del input
            else:
                # Si el servidor cierra la conexión
                break
        except:
            print("Error recibiendo datos del servidor.")
            break

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 8000
    
    try:
        client.connect((server_ip, server_port))
        print("Conectado al servidor.")

        # --- AQUÍ ESTÁ EL CAMBIO CLAVE ---
        # Creamos un hilo para recibir mensajes mientras nosotros escribimos
        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.daemon = True # Esto hace que el hilo muera si cerramos el programa
        receive_thread.start()

        while True:
            msg = input("Enter message: ")
            if msg.lower() == "close":
                client.send("close".encode("utf-8"))
                break
            
            client.send(msg.encode("utf-8"))
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    run_client()
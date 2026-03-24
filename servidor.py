import socket
import threading

# 1. Creamos una lista para almacenar los sockets de todos los conectados
clients = []

def broadcast(message, current_client_socket):
    """Envía el mensaje a todos los clientes, excepto al que lo envió."""
    for client in clients:
        if client != current_client_socket:
            try:
                # El mensaje ya viene en bytes desde el handle_client
                client.send(message)
            except:
                # Si hay error (cliente desconectado), lo removemos
                if client in clients:
                    clients.remove(client)

def handle_client(client_socket, addr):
    # Al entrar a la función, agregamos al cliente a nuestra lista global
    clients.append(client_socket)
    
    try:
        while True:
            # Recibimos los datos (en bytes)
            data = client_socket.recv(1024)
            if not data:
                break
                
            request = data.decode("utf-8")
            
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break
            
            print(f"Mensaje de {addr}: {request}")
            
            # --- EL CAMBIO CLAVE ---
            # En lugar de responder "accepted", difundimos el mensaje original a todos
            broadcast(data, client_socket)
            
    except Exception as e:
        print(f"Error al manejar cliente {addr}: {e}")
    finally:
        # Al terminar, quitamos al cliente de la lista y cerramos su socket
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()
        print(f"Conexión con {addr} cerrada y removida de la lista")


def run_server():
    server_ip = "127.0.0.1"
    port = 8000
    
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Evita el error de "Address already in use" al reiniciar rápido
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        server.bind((server_ip, port))
        server.listen()
        print(f"Servidor de Chat escuchando en {server_ip}:{port}")

        while True:
            client_socket, addr = server.accept()
            print(f"Conexión aceptada de {addr}")
            
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
            thread.start()
            # Opcional: ver cuántos usuarios hay activos
            print(f"Usuarios activos: {len(clients)}")
            
    except Exception as e:
        print(f"Error en el servidor: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    run_server()
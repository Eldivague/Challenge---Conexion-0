import socket
import threading

#  Creamos una lista para almacenar los sockets de todos los conectados
clientes = []

def broadcast(message, actual_cliente_socket):
    # Envía el mensaje a todos los clientes, excepto al que lo envió.
    for cliente in clientes:
        if cliente != actual_cliente_socket:
            try:
                # El mensaje ya viene en bytes desde el manejo_de_clientes
                cliente.send(message)
            except:
                # Si hay error (cliente desconectado), lo removemos
                if cliente in clientes:
                    clientes.remove(cliente)

def manejo_de_clientes(cliente_socket, addr):
    # Al entrar a la función, agregamos al cliente a nuestra lista global
    clientes.append(cliente_socket)
    
    try:
        while True:
            # Recibimos los datos (en bytes)
            data = cliente_socket.recv(1024)
            if not data:
                break
                
            request = data.decode("utf-8")
            
            if request.lower() == "close":
                cliente_socket.send("closed".encode("utf-8"))
                break
            
            print(f"Mensaje de {addr}: {request}")
            
            # En lugar de responder "accepted", difundimos el mensaje original a todos
            broadcast(data, cliente_socket)
            
    except Exception as error:
        print(f"Error al manejar cliente {addr}: {error}")
    finally:
        # Al terminar, quitamos al cliente de la lista y cerramos su socket
        if cliente_socket in clientes:
            clientes.remove(cliente_socket)
        cliente_socket.close()
        print(f"Conexión con {addr} cerrada y removida de la lista")


# Se crea el servidor 
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
            cliente_socket, addr = server.accept()
            print(f"Conexión aceptada de {addr}")
            
            thread = threading.Thread(target=manejo_de_clientes, args=(cliente_socket, addr,))
            thread.start()
            # Opcional: ver cuántos usuarios hay activos
            print(f"Usuarios activos: {len(clientes)}")
            
    except Exception as error:
        print(f"Error en el servidor: {error}")
    finally:
        server.close()

if __name__ == "__main__":
    run_server()
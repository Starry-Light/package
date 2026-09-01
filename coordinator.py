import socket
import threading

busy = False
queue = []
lock = threading.Lock()

def handle_client(client):
    global busy

    while True:
        message = client.recv(1024).decode()

        if not message:
            break

        with lock:
            if message == "REQUEST":
                if not busy:
                    busy = True
                    client.sendall("GRANT".encode())
                else:
                    queue.append(client)

            elif message == "RELEASE":
                if queue:
                    next_client = queue.pop(0)
                    next_client.sendall("GRANT".encode())
                else:
                    busy = False

    client.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), 12345))
server_socket.listen()

print("Coordinator is running...")

while True:
    client_socket, addr = server_socket.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket,)
    )
    thread.start()
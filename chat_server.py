import socket
import threading

clients = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.sendall(message)


def handle_client(client_socket):
    while True:
        message = client_socket.recv(1024)
        if message.decode() == "exit":
            break
        broadcast(message, client_socket)

    clients.remove(client_socket)

    client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((socket.gethostname(), 12345))

server_socket.listen()

print("Server has started")


while True:
    client_socket, addr = server_socket.accept()

    print("Connected to ", addr)
    clients.append(client_socket)
    thread = threading.Thread(target=handle_client, args=(client_socket,))

    thread.start()
